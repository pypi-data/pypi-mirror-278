from nvflare.apis.dxo import DXO, DataKind, from_shareable
from nvflare.apis.filter import Filter
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.app_constant import AppConstants
import hashlib

from oasysnow.federated.common.attestation_service.verification import (
    VerificationServer,
)


class FilterData(Filter):

    def __init__(self):
        super().__init__()

    def process(self, shareable: Shareable, fl_ctx: FLContext) -> Shareable:
        client_name = fl_ctx.get_identity_name()
        current_round = shareable.get_cookie(AppConstants.CONTRIBUTION_ROUND)

        try:
            dxo = from_shareable(shareable)
        except:
            self.log_exception(fl_ctx, "shareable data is not a valid DXO")
            return shareable

        assert isinstance(dxo, DXO)
        if dxo.data_kind not in (DataKind.WEIGHT_DIFF, DataKind.WEIGHTS):
            self.log_debug(fl_ctx, "I cannot handle {}".format(dxo.data_kind))
            return shareable

        if dxo.data is None:
            self.log_debug(fl_ctx, "no data to filter")
            return shareable

        nonce = fl_ctx.get_prop("nonce")
        server_nonce = dxo.get_meta_prop(f"nonce_{client_name}")
        if not nonce == server_nonce:
            raise Exception(">>>>>>>>ERROR nonce != server_nonce", nonce, server_nonce)

        public_key_server_bytes = dxo.get_meta_prop(f"server_pk_{client_name}")
        attestation_report = dxo.get_meta_prop(f"attestation_report_{client_name}")

        # TODO: check if the hash of public key of server from attestation report is equal to public_key_server_b64
        if not public_key_server_bytes or not attestation_report:
            raise Exception("Attestation Failed: NO public key or Report")
        fl_ctx.set_prop("server_pk", public_key_server_bytes, private=True)

        public_key_server_hash = hashlib.sha256(public_key_server_bytes).hexdigest()
        attestation_service = VerificationServer(audience=client_name, nonces=[nonce, public_key_server_hash])
        verified_attestation = attestation_service.verify(attestation_report)
        if not verified_attestation:
            raise Exception("Attestation Failed: Invalid report")

        # TODO: replace dxo.get_meta_prop with direct fl_ctx.get_peer_context

        return shareable

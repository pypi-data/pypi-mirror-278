from nvflare.apis.dxo import DXO, DataKind, from_shareable
from nvflare.apis.filter import Filter
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
import hashlib

from oasysnow.federated.common.attestation_service.verification import (
    VerificationServer,
)


class FilterData(Filter):

    def __init__(self):
        super().__init__()

    def process(self, shareable: Shareable, fl_ctx: FLContext) -> Shareable:

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


        client_name = fl_ctx.get_identity_name()
        client_nonce = fl_ctx.get_prop("nonce")
        if not client_nonce or not client_name:
            raise Exception("Client is invalid.")
        client_nonce_hash = hashlib.sha256(client_nonce.encode('utf-8')).hexdigest()

        # TODO: maybe replace dxo.get_meta_prop with direct fl_ctx.get_peer_context
        public_key_server_bytes = dxo.get_meta_prop(f"server_pk_{client_name}")
        attestation_report = dxo.get_meta_prop(f"attestation_report_{client_name}")

        if not public_key_server_bytes or not attestation_report:
            raise Exception("Attestation Failed: NO public key or Report")
        fl_ctx.set_prop("server_pk", public_key_server_bytes, private=True)

        public_key_server_hash = hashlib.sha256(public_key_server_bytes).hexdigest()
        attestation_service = VerificationServer(audience=client_name, nonce=client_nonce_hash, server_pk_hash=public_key_server_hash)
        verified_attestation = attestation_service.verify(attestation_report)
        if not verified_attestation:
            raise Exception("Attestation Failed: Invalid report")


        return shareable

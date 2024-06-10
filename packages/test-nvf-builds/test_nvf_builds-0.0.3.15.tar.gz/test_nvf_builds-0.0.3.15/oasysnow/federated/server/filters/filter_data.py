from cryptography.hazmat.primitives.asymmetric import ec
import cryptography.hazmat.primitives.serialization as ser
from nvflare.apis.dxo import DXO, DataKind, from_shareable
from nvflare.apis.filter import Filter
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.app_constant import AppConstants
import hashlib

from oasysnow.federated.common.attestation_service.server import AttestationServer


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


        contributor_name = fl_ctx.get_peer_context().get_identity_name()
        client_nonce = fl_ctx.get_peer_context().get_prop("nonce")
        current_round = shareable.get_cookie(AppConstants.CONTRIBUTION_ROUND)

        private_key_server = ec.generate_private_key(ec.SECP384R1())
        public_key_server_bytes = private_key_server.public_key().public_bytes(ser.Encoding.PEM, ser.PublicFormat.SubjectPublicKeyInfo)
        public_key_server_hash = hashlib.sha256(public_key_server_bytes).hexdigest()

        attestation_service = AttestationServer()
        attestation_report = attestation_service.get_custom_attestation(nonces=[str(client_nonce), public_key_server_hash], audience=contributor_name)

        fl_ctx.set_prop(f"server_sk_{contributor_name}", private_key_server, private=True)

        # TODO: replace dxo.get_meta_prop with direct fl_ctx.get_peer_context
        fl_ctx.set_prop(f"test", f"{current_round}:{client_nonce}", False, False)

        dxo.set_meta_prop(f"server_pk_{contributor_name}", public_key_server_bytes)
        dxo.set_meta_prop(f"nonce_{contributor_name}", client_nonce)
        dxo.set_meta_prop(f"attestation_report_{contributor_name}", attestation_report)


        return dxo.update_shareable(shareable)

import base64
import pickle

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import cryptography.hazmat.primitives.serialization as ser
from nvflare.apis.dxo import DXO, DataKind, from_shareable
from nvflare.apis.filter import Filter
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable

class FilterResults(Filter):

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

        client_pk_bytes = dxo.get_meta_prop("client_pk")
        if not client_pk_bytes:
            raise Exception("No public key found for this client")

        private_key_server = fl_ctx.get_prop(f"server_sk_{contributor_name}")
        if not private_key_server:
            raise Exception(f"Can not derive the shared key for client {contributor_name}")

        client_pk = ser.load_pem_public_key(client_pk_bytes)
        shared_key_server = private_key_server.exchange(ec.ECDH(), client_pk)
        derived_key_server = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"handshake").derive(shared_key_server)

        f_server = Fernet(base64.b64encode(derived_key_server))
        enc_data = dxo.data['weights_enc']
        data_bytes = f_server.decrypt(enc_data)
        weights = pickle.loads(data_bytes)

        dxo.data = weights

        return dxo.update_shareable(shareable)

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

        public_key_server_bytes = fl_ctx.get_prop(f"server_pk")
        if not public_key_server_bytes:
            raise Exception("Attestation Failed!", public_key_server_bytes)
        server_pk = ser.load_pem_public_key(public_key_server_bytes)

        private_key = ec.generate_private_key(ec.SECP384R1())
        public_key_bytes = private_key.public_key().public_bytes(ser.Encoding.PEM, ser.PublicFormat.SubjectPublicKeyInfo)
        shared_key_client = private_key.exchange(ec.ECDH(), server_pk)
        derived_key_client = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"handshake").derive(shared_key_client)

        f_client = Fernet(base64.b64encode(derived_key_client))
        weights = dxo.data
        weights_bytes = pickle.dumps(weights)
        weights_enc = f_client.encrypt(weights_bytes)

        dxo.data = {'weights_enc': weights_enc}
        dxo.set_meta_prop("client_pk", public_key_bytes)


        return dxo.update_shareable(shareable)

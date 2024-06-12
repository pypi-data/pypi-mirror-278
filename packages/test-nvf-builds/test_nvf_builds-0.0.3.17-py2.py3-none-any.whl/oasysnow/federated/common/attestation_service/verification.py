import json
import jwt
import requests



class VerificationServer:
    def __init__(self, audience: str, nonce:str, server_pk_hash: str):
        self.audience = audience
        self.nonce = nonce
        self.server_pk_hash = server_pk_hash

    def verify(self, report: str) -> bool:
        try:
            issuer_url = "https://confidentialcomputing.googleapis.com/.well-known/openid-configuration"
            issuer = json.loads(requests.get(issuer_url).text)
            jwks_uri = issuer['jwks_uri']
            supported_algs = issuer['id_token_signing_alg_values_supported']
            supported_algs = issuer['id_token_signing_alg_values_supported']
            jwks_client = jwt.PyJWKClient(jwks_uri)
            signing_key = jwks_client.get_signing_key_from_jwt(report)
            data = jwt.decode(
                report,
                signing_key.key,
                algorithms=supported_algs,
                audience=self.audience,
            )
            if data['eat_nonce'][0] != self.nonce:
                raise Exception("Nonce mismatch error.")
            if data['eat_nonce'][1] != self.server_pk_hash:
                raise Exception("Server public key digest mismatch error.")
            
            print(json.dumps(data, indent=2))
            print('>>>>>> Attestation SUCCEEDED')
            return True
        except Exception as e:
            print('>>>>>> Attestation FAILED')
            print(e)
            return False







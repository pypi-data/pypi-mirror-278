import json
from typing import List

import jwt
import requests



class VerificationServer:
    def __init__(self, audience: str, nonces: List[str]):
        self.audience = audience
        self.nonces = nonces

    def verify(self, report: str) -> bool:
        try:
            print(">>>>report", report)
            issuer_url = "https://confidentialcomputing.googleapis.com/.well-known/openid-configuration"
            issuer = json.loads(requests.get(issuer_url).text)
            jwks_uri = issuer['jwks_uri']
            supported_algs = issuer['id_token_signing_alg_values_supported']
            optional_custom_headers = {"User-agent": "custom-user-agent"}
            supported_algs = issuer['id_token_signing_alg_values_supported']
            jwks_client = jwt.PyJWKClient(jwks_uri, headers=optional_custom_headers)
            signing_key = jwks_client.get_signing_key_from_jwt(report)
            data = jwt.decode(
                report,
                signing_key.key,
                algorithms=supported_algs,
                audience=self.audience,
            )
            print(json.dumps(data, indent=2))
            print('>>>>>> Attestation SUCCEEDED')
            return True
        except Exception as e:
            print('>>>>>> Attestation FAILED')
            print(e)
            return False







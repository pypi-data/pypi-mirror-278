import http.client
import json
import socket
from typing import List
import threading


class AttestationServer:
    _lock = threading.Lock()

    def __init__(self):
        self.options = {
            "socketPath": "/run/container_launcher/teeserver.sock",
            "host": "localhost",
            "path": "/v1/token",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
            },
        }

    def get_custom_attestation(self, nonces: List[str], audience: str):
        token_request = {"nonces": nonces, "audience": audience, "token_type": "OIDC"}
        custom_json = json.dumps(token_request).encode("utf-8")
        self.options["headers"]["Content-Length"] = len(custom_json)

        with AttestationServer._lock:
            response = self._make_request(custom_json)

        print(">>>>get_custom_attestation", audience, nonces)
        print(">>>>AttestationServer", response)
        return response

    def _make_request(self, custom_json):
        if "socketPath" in self.options:
            conn = http.client.HTTPConnection(
                self.options["host"],
                port=http.client.HTTPConnection.default_port,
            )
            conn.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            conn.sock.connect(self.options["socketPath"])
        else:
            conn = http.client.HTTPConnection(self.options["host"])

        try:
            conn.request(
                self.options["method"],
                self.options["path"],
                body=custom_json,
                headers=self.options["headers"],
            )
            response = conn.getresponse()
            data = response.read().decode()
            conn.close()
            return data
        except Exception as e:
            conn.close()
            raise e

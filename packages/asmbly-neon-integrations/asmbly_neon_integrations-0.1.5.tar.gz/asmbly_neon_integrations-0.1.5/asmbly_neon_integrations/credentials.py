"""Credentials interface for APIs"""

# pylint: disable=missing-class-docstring

import base64
from dataclasses import dataclass


@dataclass
class NeonCredentials:
    api_user: str
    api_key: str

    @property
    def headers(self):
        """Get get the authorization headers for API requests"""

        n_auth = f"{self.api_user}:{self.api_key}"
        n_signature = base64.b64encode(bytearray(n_auth.encode())).decode()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Basic {n_signature}",
        }


@dataclass
class AltaCredentials:
    api_user: str
    api_key: str

    @property
    def headers(self):
        """Get get the authorization headers for API requests"""

        o_auth = f"{self.api_user}:{self.api_key}"
        # Asmbly is OpenPath org ID 5231
        o_signature = base64.b64encode(bytearray(o_auth.encode())).decode()
        return {
            "Authorization": f"Basic {o_signature}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }


@dataclass
class GmailCredentials:
    username: str
    password: str


@dataclass
class FlodeskCredentials:
    api_key: str

    @property
    def headers(self):
        """Get get the authorization headers for API requests"""

        auth = f"{self.api_key}:"
        signature = base64.b64encode(bytearray(auth.encode())).decode()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Basic {signature}",
        }

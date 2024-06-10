import os
from dataclasses import dataclass


@dataclass
class Credentials:
    neon_api_user: str
    neon_api_key: str
    op_api_user: str
    op_api_key: str
    gmail_user: str
    gmail_pass: str
    flodesk_api_key: str | None


def get_creds() -> Credentials:
    credentials = Credentials(
        neon_api_user=os.environ.get("N_API_USER"),
        neon_api_key=os.environ.get("N_API_KEY"),
        op_api_user=os.environ.get("O_API_USER"),
        op_api_key=os.environ.get("O_API_KEY"),
        gmail_user=os.environ.get("GMAIL_USER"),
        gmail_pass=os.environ.get("GMAIL_PASS"),
        flodesk_api_key=os.environ.get("FLODESK_API_KEY"),
    )

    return credentials

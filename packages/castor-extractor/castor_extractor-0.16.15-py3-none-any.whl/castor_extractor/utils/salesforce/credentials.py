from typing import Dict

from ...utils import from_env
from .constants import Keys

_USERNAME = "CASTOR_SALESFORCE_USERNAME"
_PASSWORD = "CASTOR_SALESFORCE_PASSWORD"  # noqa: S105
_SECURITY_TOKEN = "CASTOR_SALESFORCE_SECURITY_TOKEN"  # noqa: S105
_CLIENT_ID = "CASTOR_SALESFORCE_CLIENT_ID"
_CLIENT_SECRET = "CASTOR_SALESFORCE_CLIENT_SECRET"  # noqa: S105
_BASE_URL = "CASTOR_SALESFORCE_BASE_URL"


class SalesforceCredentials:
    """
    Class to handle Salesforce rest API permissions
    """

    def __init__(
        self,
        *,
        username: str,
        password: str,
        security_token: str,
        client_id: str,
        client_secret: str,
        base_url: str,
    ):
        self.username = username
        self.password = password + security_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url

    def token_request_payload(self) -> Dict[str, str]:
        """
        Params to post to the API in order to retrieve the authentication token
        """
        return {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": self.password,
        }


def to_credentials(params: dict) -> SalesforceCredentials:
    """extract Salesforce credentials"""
    username = params.get(Keys.USERNAME) or from_env(_USERNAME)
    password = params.get(Keys.PASSWORD) or from_env(_PASSWORD)
    security_token = params.get(Keys.SECURITY_TOKEN) or from_env(
        _SECURITY_TOKEN
    )
    client_id = params.get(Keys.CLIENT_ID) or from_env(_CLIENT_ID)
    client_secret = params.get(Keys.CLIENT_SECRET) or from_env(_CLIENT_SECRET)
    base_url = params.get(Keys.BASE_URL) or from_env(_BASE_URL)
    return SalesforceCredentials(
        username=username,
        password=password,
        client_id=client_id,
        client_secret=client_secret,
        security_token=security_token,
        base_url=base_url,
    )

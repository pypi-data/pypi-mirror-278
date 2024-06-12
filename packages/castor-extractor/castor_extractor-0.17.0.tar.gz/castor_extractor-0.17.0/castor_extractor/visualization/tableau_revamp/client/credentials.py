from enum import Enum
from typing import Dict, Literal, Optional, overload

from ....utils import from_env

_AUTH_ERROR_MSG = "Need either user and password or token_name and token"

# To specify the default site on Tableau Server, you can use an empty string
# https://tableau.github.io/server-client-python/docs/api-ref#authentication
_DEFAULT_SERVER_SITE_ID = ""


class CredentialsKey(Enum):
    """Value enum object for the credentials"""

    TABLEAU_USER = "user"
    TABLEAU_PASSWORD = "password"  # noqa: S105
    TABLEAU_TOKEN_NAME = "token_name"  # noqa: S105
    TABLEAU_TOKEN = "token"  # noqa: S105
    TABLEAU_SITE_ID = "site_id"
    TABLEAU_SERVER_URL = "server_url"


CREDENTIALS_ENV: Dict[CredentialsKey, str] = {
    CredentialsKey.TABLEAU_USER: "CASTOR_TABLEAU_USER",
    CredentialsKey.TABLEAU_PASSWORD: "CASTOR_TABLEAU_PASSWORD",
    CredentialsKey.TABLEAU_TOKEN_NAME: "CASTOR_TABLEAU_TOKEN_NAME",
    CredentialsKey.TABLEAU_TOKEN: "CASTOR_TABLEAU_TOKEN",
    CredentialsKey.TABLEAU_SITE_ID: "CASTOR_TABLEAU_SITE_ID",
    CredentialsKey.TABLEAU_SERVER_URL: "CASTOR_TABLEAU_SERVER_URL",
}


@overload
def get_value(key: CredentialsKey, kwargs: dict) -> Optional[str]: ...


@overload
def get_value(
    key: CredentialsKey, kwargs: dict, optional: Literal[True]
) -> Optional[str]: ...


@overload
def get_value(
    key: CredentialsKey, kwargs: dict, optional: Literal[False]
) -> str: ...


def get_value(
    key: CredentialsKey,
    kwargs: dict,
    optional: bool = True,
) -> Optional[str]:
    """
    Returns the value of the given key:
    - from kwargs in priority
    - from ENV otherwise
    Raises an error if not found (unless optional)
    """

    if key.value in kwargs:
        return kwargs[key.value]

    env_key = CREDENTIALS_ENV[key]
    return from_env(env_key, optional)


class TableauRevampCredentials:
    """
    Tableau's credentials to connect to REST API
    """

    def __init__(
        self,
        *,
        server_url: str,
        site_id: Optional[str],
        user: Optional[str],
        password: Optional[str],
        token_name: Optional[str],
        token: Optional[str],
    ):
        self.user = user
        self.site_id = site_id or _DEFAULT_SERVER_SITE_ID
        self.server_url = server_url
        self.password = password
        self.token_name = token_name
        self.token = token

    @classmethod
    def from_env(cls, kwargs: dict) -> "TableauRevampCredentials":
        return TableauRevampCredentials(
            server_url=get_value(
                CredentialsKey.TABLEAU_SERVER_URL,
                kwargs,
                optional=False,
            ),
            site_id=get_value(CredentialsKey.TABLEAU_SITE_ID, kwargs),
            user=get_value(CredentialsKey.TABLEAU_USER, kwargs),
            password=get_value(CredentialsKey.TABLEAU_PASSWORD, kwargs),
            token_name=get_value(CredentialsKey.TABLEAU_TOKEN_NAME, kwargs),
            token=get_value(CredentialsKey.TABLEAU_TOKEN, kwargs),
        )

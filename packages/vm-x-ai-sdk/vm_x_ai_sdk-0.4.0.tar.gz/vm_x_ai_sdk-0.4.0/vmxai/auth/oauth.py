from typing import TYPE_CHECKING, Generic, Optional, TypedDict, TypeVar

from cachetools import Cache, TTLCache
from requests import post

from vmxai.auth.provider import VMXClientAuthProvider

if TYPE_CHECKING:
    from vmxai.client import VMXClient

T = TypeVar("T", bound=Cache)


class OAuthTokenResult(TypedDict):
    access_token: str
    expires_in: int
    token_type: str


class VMXClientOAuth(Generic[T], VMXClientAuthProvider):
    def __init__(self, client_id: str, client_secret: str, cache_manager: Optional[T] = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.cache = cache_manager or TTLCache(
            maxsize=100,
            ttl=3540,
        )  # 59 minutes

    def inject_credentials(self, client: "VMXClient", grpc_metadata: list[tuple[str, str]]) -> tuple[tuple[str, str]]:
        token = self.get_oauth_token(client.domain)
        grpc_metadata.append(("authorization", f"Bearer {token}"))
        return grpc_metadata

    def get_oauth_token(self, domain: str) -> str:
        token = self.cache.get("oauth_token")
        if token:
            return token

        response = post(
            f"https://auth.{domain}/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )

        result: OAuthTokenResult = response.json()
        self.cache["oauth_token"] = result["access_token"]

        return result["access_token"]

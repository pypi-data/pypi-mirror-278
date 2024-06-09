"""Main module."""

from typing import Optional

import aiohttp
import requests
import urllib3

from synthientpy.constants import API_URL, DEFAULT_TIMEOUT
from synthientpy.exceptions import ErrorResponse, InternalServerError
from synthientpy.models import DeleteResponse, LookupResponse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Client:
    """Synchronous client for interacting with the Synthient API."""

    def __init__(
        self,
        api_key: str,
        default_timeout: int = DEFAULT_TIMEOUT,
        proxy: Optional[str] = None,
    ):
        self._http = requests.Session()
        self._http.headers = {"Authorization": api_key}
        if proxy:
            self._http.proxies = {"http": proxy, "https": proxy}
            self._http.verify = False
        self.default_timeout: int = default_timeout

    def lookup(self, token: str) -> "LookupResponse":
        """Lookup a token and return it's corresponding data.

        Args:
            token (str): Token to lookup.

        Raises:
            Union[ErrorResponse, InternalServerError]: If the server returns a 401 or 400.

        Returns:
            LookupResponse: The token data. See docs.synthient.com/api for more information.
        """
        resp = self._http.get(f"{API_URL}lookup/{token}", timeout=self.default_timeout)
        if resp.status_code == 200:
            return LookupResponse(**resp.json())
        elif resp.status_code in (401, 409):
            json = resp.json()
            raise ErrorResponse(json["message"])
        else:
            raise InternalServerError("Server failed to lookup token.")

    def delete(self, token: str) -> DeleteResponse:
        """Delete a token.

        Args:
            token (str): Token to delete.
        Raises:
            InternalServerError: If the server returns a 500.
        Returns:
            DeleteResponse: The response from the server.
        """
        resp = self._http.delete(
            f"{API_URL}delete/{token}", timeout=self.default_timeout
        )
        if resp.status_code == 500:
            raise InternalServerError("Server failed to delete token.")
        return DeleteResponse(**resp.json())


class AsyncClient:
    """Asynchronous client for interacting with the Synthient API."""

    def __init__(
        self,
        api_key: str,
        default_timeout: int = DEFAULT_TIMEOUT,
        proxy: Optional[str] = None,
    ):
        self.api_key: str = api_key
        self.proxy: Optional[str] = proxy
        self.default_timeout: int = default_timeout

    async def lookup(self, token: str) -> "LookupResponse":
        """Lookup a token and return it's corresponding data.

        Args:
            token (str): Token to lookup.

        Raises:
            Union[ErrorResponse, InternalServerError]: If the server returns a 401 or 400.

        Returns:
            LookupResponse: The token data. See docs.synthient.com/api for more information.
        """
        async with aiohttp.ClientSession(headers={"Authorization": self.api_key}).get(
            f"{API_URL}lookup/{token}", timeout=self.default_timeout, proxy=self.proxy
        ) as resp:
            if resp.status == 200:
                return LookupResponse(**await resp.json())
            elif resp.status in (401, 404, 409):
                json = await resp.json()
                raise ErrorResponse(json["message"])
            else:
                raise InternalServerError("Server failed to lookup token.")

    async def delete(self, token: str) -> DeleteResponse:
        """Delete a token.

        Args:
            token (str): Token to delete.
        Raises:
            InternalServerError: If the server returns a 500.
        Returns:
            DeleteResponse: The response from the server.
        """
        async with aiohttp.ClientSession(
            headers={"Authorization": self.api_key}
        ).delete(
            f"{API_URL}delete/{token}", timeout=self.default_timeout, proxy=self.proxy
        ) as resp:
            if resp.status == 500:
                raise InternalServerError("Server failed to delete token.")
            return DeleteResponse(**await resp.json())

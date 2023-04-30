"""Sample API Client."""
from __future__ import annotations
from .const import (
    GENERATED_TODAY,
    ALARMS,
    CURRENT_POWER,
    GENERATED_TOTAL,
    PATH,
    POWERED_ON,
)
import re
import asyncio
import socket
import aiohttp
import async_timeout


class DeyeIntegrationApiClientError(Exception):
    """Exception to indicate a general API error."""


class DeyeIntegrationApiClientCommunicationError(DeyeIntegrationApiClientError):
    """Exception to indicate a communication error."""


class DeyeIntegrationApiClientAuthenticationError(DeyeIntegrationApiClientError):
    """Exception to indicate an authentication error."""


class DeyeIntegrationApiClient:
    """Sample API Client."""

    def __init__(
        self, username: str, password: str, url: str, session: aiohttp.ClientSession
    ) -> None:
        """Sample API Client."""
        self._username = username
        self._password = password
        self._url = url
        self._session = session

    async def async_get_data(self) -> any:
        """Get data from the API."""

        def read_sol_data(name, data):
            matches = re.search(f'var {name} = "(.*)"', data)
            return matches.group(1)

        try:
            html = await self._api_wrapper(method="get", path=PATH)
            data = {}
            data[GENERATED_TOTAL] = read_sol_data(GENERATED_TOTAL, html)
            data[GENERATED_TODAY] = read_sol_data(GENERATED_TODAY, html)
            data[ALARMS] = (
                "0"
                if read_sol_data(ALARMS, html) == ""
                else read_sol_data(ALARMS, html)
            )
            data[CURRENT_POWER] = read_sol_data(CURRENT_POWER, html)
            data[POWERED_ON] = True
            return data

        except DeyeIntegrationApiClientAuthenticationError as exception:
            raise exception

        except Exception as exception:
            data = {}
            # data[GENERATED_TOTAL] = read_sol_data(GENERATED_TOTAL, html)
            # data[GENERATED_TODAY] = read_sol_data(GENERATED_TODAY, html)
            # data[ALARMS] = read_sol_data(ALARMS, html)
            data[CURRENT_POWER] = 0
            data[POWERED_ON] = False
            return data

    async def _api_wrapper(self, method: str, path: str) -> any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=self._url + path,
                    auth=aiohttp.BasicAuth(self._username, self._password),
                )
                if response.status in (401, 403):
                    raise DeyeIntegrationApiClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                return await response.text()

        except asyncio.TimeoutError as exception:
            raise DeyeIntegrationApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise DeyeIntegrationApiClientCommunicationError(
                "Error fetching information",
            ) from exception
        except DeyeIntegrationApiClientAuthenticationError as exception:
            raise exception
        except Exception as exception:  # pylint: disable=broad-except
            raise DeyeIntegrationApiClientError(
                "Something really wrong happened!"
            ) from exception

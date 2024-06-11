import asyncio
import importlib.metadata
from datetime import datetime
from typing import Any

from aiohttp import ClientSession

from .probe import Probe


class InvalidAuth(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class Timeout(Exception):
    pass


class CustomerApi:

    API_TIMEOUT_NORMAL = 3
    API_TIMEOUT_SLOW = 10
    DEFAULT_LANGUAGE = "en"

    api_base_url = "https://monitor.sensoterra.com/api"
    api_version = "3"

    def __init__(self, email: str | None = None, password: str | None = None):
        self.__email = email
        self.__password = password
        self.__headers = {
            "User-Agent": "Sensoterra Python API {}".format(self.get_version()),
            "language": self.DEFAULT_LANGUAGE,
        }
        self.__probes: dict[str, Probe] = {}
        self.__api_token: str | None = None

    async def __auth(self, session: ClientSession) -> None:
        """Authenticate using either email and password, or an API token"""
        if self.__api_token is None:
            async with session.post(
                f"{self.api_base_url}/v{self.api_version}/customer/auth",
                json={"email": self.__email, "password": self.__password},
                timeout=self.API_TIMEOUT_NORMAL,
            ) as resp:
                if resp.status >= 400 and resp.status <= 499:
                    json = await resp.json()
                    raise InvalidAuth(json["message"])
                resp.raise_for_status()
                json = await resp.json()
                api_key = json["api_key"]
        else:
            api_key = self.__api_token

        self.__headers["api_key"] = api_key

    async def __request(
        self,
        session: ClientSession,
        method: str,
        command: str,
        params: dict[str, str] | None = None,
        json: dict[str, str] | None = None,
    ) -> Any:
        """Wrapper to requests.request

        Returns:
        None: in case a http status 429 is received, or when poll too often
        Response: request response object
        """

        for i in range(2):
            if "api_key" not in self.__headers:
                await self.__auth(session)
            async with session.request(
                method,
                f"{self.api_base_url}/v{self.api_version}/{command}",
                headers=self.__headers,
                params=params,
                json=json,
                timeout=self.API_TIMEOUT_SLOW,
            ) as resp:
                if resp.status == 403:  # unauthorized
                    await self.__auth(session)
                    json = None
                else:
                    resp.raise_for_status()
                    json = await resp.json()
                    break

        return json

    async def __get_locations(self, session: ClientSession) -> dict[int, str]:
        """Get all locations"""
        data = {"include_shared_data": "YES"}

        locations = await self.__request(session, "GET", "location", params=data)

        return {location["id"]: location["name"] for location in locations}

    async def __get_soils(self, session: ClientSession) -> dict[str, str]:
        """Get all soil types"""

        parameters = await self.__request(session, "GET", "parameter")

        return {
            parameter["key"]: parameter["name"]
            for parameter in parameters
            if parameter["type"] == "SOIL"
        }

    async def __get_probes(self, session: ClientSession) -> dict[str, str]:
        """Get all probes"""

        params = {"include_shared_data": "YES"}

        probes: dict[str, str] = await self.__request(
            session, "GET", "probe", params=params
        )
        return probes

    def get_version(self) -> str:
        return importlib.metadata.version("sensoterra")

    def set_language(self, language: str) -> None:
        """Set langage like for soil names

        Examples: es, en, en-us, nl
        """
        self.__headers["language"] = language

    def set_token(self, token: str) -> None:
        self.__api_token = token

    async def get_token(self, tag: str, scope: str, expiration: datetime) -> str:
        async with ClientSession() as session:
            data = {
                "tag": tag,
                "scope": scope,
                "expiration": expiration.astimezone().isoformat(),
            }
            json = await self.__request(session, "POST", "token", json=data)
        return str(json["token"])

    async def poll(self) -> list[Probe]:
        """Update the list of probes"""
        try:
            async with ClientSession() as session:
                await self.__auth(session)
                async with asyncio.TaskGroup() as tg:
                    task_1 = tg.create_task(self.__get_probes(session))
                    task_2 = tg.create_task(self.__get_soils(session))
                    task_3 = tg.create_task(self.__get_locations(session))
                probes: list[dict[str, Any]] = task_1.result()  # type: ignore
                soils = task_2.result()
                locations = task_3.result()
        except ExceptionGroup as exp:
            for inner in exp.exceptions:
                if isinstance(inner, TimeoutError):
                    raise Timeout
            raise exp

        for probe in probes:
            if probe["serial"] not in self.__probes:
                self.__probes[probe["serial"]] = Probe()
            self.__probes[probe["serial"]].update(soils, locations, probe)

        return list(self.__probes.values())

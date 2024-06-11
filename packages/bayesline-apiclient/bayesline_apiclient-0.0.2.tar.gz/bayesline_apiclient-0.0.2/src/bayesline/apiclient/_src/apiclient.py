import asyncio
import functools
import json
import os
import time
from http import HTTPStatus
from typing import Any, Literal

import httpx
from pydantic import BaseModel

_CLIENT_ERROR_CODES = set(range(400, 500))
_SERVER_ERROR_CODES = set(range(500, 600))
_DEFAULT_TIMEOUT = httpx.Timeout(
    None,
    connect=int(os.getenv("BAYESLINE_APICLIENT_CONNECT_TIMEOUT", 60)),
    read=int(os.getenv("BAYESLINE_APICLIENT_READ_TIMEOUT", 60)),
    write=int(os.getenv("BAYESLINE_APICLIENT_WRITE_TIMEOUT", 60)),
)
_TASK_TIMEOUT = int(os.getenv("BAYESLINE_APICLIENT_TASK_TIMEOUT", 120))


class ApiClientError(Exception):
    pass


class ApiServerError(Exception):
    pass


class ThisIsATaskException(Exception):

    def __init__(self, response: httpx.Response, args):
        self.response = response
        self.args = args


class BaseApiClient:

    def __init__(
        self,
        endpoint: str,
        *,
        auth_str: str,
        auth_type: Literal["BEARER", "API_KEY"] = "API_KEY",
        base_path: str | None = None,
    ):
        assert (
            endpoint.strip() == "" or endpoint.strip()[-1] != "/"
        ), "endpoint should not end with a slash"
        assert (
            not base_path or base_path.strip()[-1] != "/"
        ), "base_path should not end with a slash"
        assert (
            not base_path or base_path.strip()[0] != "/"
        ), "base_path should not start with a slash"
        self.endpoint = endpoint.strip()
        self.auth_str = auth_str
        self.auth_type = auth_type
        self.base_path = "" if not base_path else base_path.strip()

    def make_url(self, url: str, endpoint: bool = True) -> str:
        if url.startswith("/"):
            url = url[1:]

        result = []
        if endpoint:
            result.append(self.endpoint)
        if self.base_path:
            result.append(self.base_path)
        if url:
            result.append(url)

        return "/".join(result)

    def _make_params_and_headers(
        self, params: dict[str, Any] | None
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        params = params or {}
        if self.auth_type == "BEARER":
            return params, {"Authorization": f"Bearer {self.auth_str}"}
        else:
            return {**params, "api_key": self.auth_str}, {}

    def __str__(self) -> str:
        endpoint, base_path = self.endpoint, self.base_path
        return f"{self.__class__.__name__}(endpoint={endpoint}, auth=***, auth_stype={self.auth_type}, base_path={base_path})"

    def __repr__(self) -> str:
        return str(self)


class ApiClient(BaseApiClient):

    def __init__(
        self,
        endpoint: str,
        *,
        auth_str: str,
        auth_type: Literal["BEARER", "API_KEY"] = "API_KEY",
        base_path: str | None = None,
        client: httpx.Client | None = None,
    ):
        super().__init__(
            endpoint, auth_str=auth_str, auth_type=auth_type, base_path=base_path
        )
        self.request_executor = client or httpx.Client(
            follow_redirects=True, timeout=_DEFAULT_TIMEOUT
        )

    def with_base_path(self, base_path: str) -> "ApiClient":
        return ApiClient(
            self.endpoint,
            auth_str=self.auth_str,
            auth_type=self.auth_type,
            base_path=base_path,
            client=self.request_executor,
        )

    def append_base_path(self, base_path: str) -> "ApiClient":
        return ApiClient(
            self.endpoint,
            auth_str=self.auth_str,
            auth_type=self.auth_type,
            base_path=self.make_url(base_path, endpoint=False),
            client=self.request_executor,
        )

    def get(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:  # noqa: ANN401
        params, headers = self._make_params_and_headers(params)
        try:
            return self.raise_for_status(self.request_executor.get)(
                self.make_url(url) if not absolute_url else url,
                params=params,
                headers=headers,
            )
        except ThisIsATaskException as e:
            return self.wait_for_task(e.response, e.args)

    def head(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:  # noqa: ANN401
        params, headers = self._make_params_and_headers(params)
        try:
            return self.raise_for_status(self.request_executor.head)(
                self.make_url(url) if not absolute_url else url,
                params=params,
                headers=headers,
            )
        except ThisIsATaskException as e:
            return self.wait_for_task(e.response, e.args)

    def post(
        self,
        url: str,
        json: dict[str, Any] | BaseModel | None,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        absolute_url: bool = False,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(params)
        if json is not None and data is not None:
            raise ValueError("Only one of json or data should be provided")
        elif json is None and data is None:
            raise ValueError("Either json or data should be provided")

        if isinstance(json, BaseModel):
            kwargs = {"data": json.model_dump_json()}
        elif data is not None:
            kwargs = {"data": data}
        else:
            kwargs = {"json": json}  # type: ignore

        try:
            return self.raise_for_status(self.request_executor.post)(
                self.make_url(url) if not absolute_url else url,
                params=params,
                headers=headers,
                **kwargs,
            )
        except ThisIsATaskException as e:
            return self.wait_for_task(e.response, e.args)

    def put(
        self,
        url: str,
        json: dict[str, Any] | BaseModel,
        params: dict[str, Any] | None = None,
        absolute_url: bool = False,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(params)
        if isinstance(json, BaseModel):
            kwargs = {"data": json.model_dump_json()}
        else:
            kwargs = {"json": json}  # type: ignore

        try:
            return self.raise_for_status(self.request_executor.put)(
                self.make_url(url) if not absolute_url else url,
                params=params,
                headers=headers,
                **kwargs,
            )
        except ThisIsATaskException as e:
            return self.wait_for_task(e.response, e.args)

    def delete(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        absolute_url: bool = False,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(params)
        try:
            return self.raise_for_status(self.request_executor.delete)(
                self.make_url(url) if not absolute_url else url,
                params=params,
                headers=headers,
            )
        except ThisIsATaskException as e:
            return self.wait_for_task(e.response, e.args)

    def wait_for_task(self, response: httpx.Response, args) -> httpx.Response:
        message = response.json()
        task_id = message["task_id"]
        status_location = response.headers.get("location")
        seconds_passed = 0
        while message["status"] not in {"completed", "failed"}:
            time.sleep(1)
            message = self.get(
                f"{self.endpoint}/{status_location}", absolute_url=True
            ).json()
            seconds_passed += 1

            if seconds_passed > _TASK_TIMEOUT:
                raise Exception(f"Task {task_id} timed out. last status: {message}")

        if message["status"] == "failed":
            raise ApiServerError(f"Task {task_id} failed: {message}")

        result_url = message["result"]["content"]["url"]
        response = self.get(f"{self.endpoint}/{result_url}", absolute_url=True)
        handle_response(response, args)
        return response

    @staticmethod
    def raise_for_status(fn):  # noqa: ANN202, ANN001
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):  # noqa: ANN202, ANN002, ANN003
            response = None
            try:
                response = fn(
                    *args,
                    timeout=_DEFAULT_TIMEOUT,
                    **kwargs,
                )  # typing: ignore
            finally:
                handle_response(response, args)

            if response is not None and response.status_code == HTTPStatus.ACCEPTED:
                # this is a task that is being processed
                raise ThisIsATaskException(response, args)

            return response

        return wrapped


class AsyncApiClient(BaseApiClient):

    def __init__(
        self,
        endpoint: str,
        *,
        auth_str: str,
        auth_type: Literal["BEARER", "API_KEY"] = "API_KEY",
        base_path: str | None = None,
        client: httpx.AsyncClient | None = None,
    ):
        assert (
            endpoint.strip() == "" or endpoint.strip()[-1] != "/"
        ), "endpoint should not end with a slash"
        assert (
            not base_path or base_path.strip()[-1] != "/"
        ), "base_path should not end with a slash"
        assert (
            not base_path or base_path.strip()[0] != "/"
        ), "base_path should not start with a slash"
        self.endpoint = endpoint.strip()
        self.auth_str = auth_str
        self.auth_type = auth_type
        self.base_path = "" if not base_path else base_path.strip()
        self.request_executor = client or httpx.AsyncClient(
            follow_redirects=True, timeout=_DEFAULT_TIMEOUT
        )

    def with_base_path(self, base_path: str) -> "AsyncApiClient":
        return AsyncApiClient(
            self.endpoint,
            auth_str=self.auth_str,
            auth_type=self.auth_type,
            base_path=base_path,
            client=self.request_executor,
        )

    def append_base_path(self, base_path: str) -> "AsyncApiClient":
        return AsyncApiClient(
            self.endpoint,
            auth_str=self.auth_str,
            auth_type=self.auth_type,
            base_path=self.make_url(base_path, endpoint=False),
            client=self.request_executor,
        )

    async def get(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:  # noqa: ANN401
        params, headers = self._make_params_and_headers(params)
        try:
            return await self.raise_for_status(self.request_executor.get)(
                self.make_url(url) if not absolute_url else url,
                params=params,
                headers=headers,
            )
        except ThisIsATaskException as e:
            return await self.wait_for_task(e.response, e.args)

    async def head(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:  # noqa: ANN401
        params, headers = self._make_params_and_headers(params)
        try:
            return await self.raise_for_status(self.request_executor.head)(
                self.make_url(url) if not absolute_url else url,
                params=params,
                headers=headers,
            )
        except ThisIsATaskException as e:
            return await self.wait_for_task(e.response, e.args)

    async def post(
        self,
        url: str,
        json: dict[str, Any] | BaseModel | None,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        absolute_url: bool = False,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(params)
        if json is not None and data is not None:
            raise ValueError("Only one of json or data should be provided")
        elif json is None and data is None:
            raise ValueError("Either json or data should be provided")

        if isinstance(json, BaseModel):
            kwargs = {"data": json.model_dump_json()}
        elif data is not None:
            kwargs = {"data": data}
        else:
            kwargs = {"json": json}  # type: ignore

        try:
            return await self.raise_for_status(self.request_executor.post)(
                self.make_url(url) if not absolute_url else url,
                params=params,
                headers=headers,
                **kwargs,
            )
        except ThisIsATaskException as e:
            return await self.wait_for_task(e.response, e.args)

    async def put(
        self,
        url: str,
        json: dict[str, Any] | BaseModel,
        params: dict[str, Any] | None = None,
        absolute_url: bool = False,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(params)

        if isinstance(json, BaseModel):
            kwargs = {"data": json.model_dump_json()}
        else:
            kwargs = {"json": json}  # type: ignore

        try:
            return await self.raise_for_status(self.request_executor.put)(
                self.make_url(url) if not absolute_url else url,
                params=params,
                headers=headers,
                **kwargs,
            )
        except ThisIsATaskException as e:
            return await self.wait_for_task(e.response, e.args)

    async def delete(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        absolute_url: bool = False,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(params)
        try:
            return await self.raise_for_status(self.request_executor.delete)(
                self.make_url(url) if not absolute_url else url,
                params=params,
                headers=headers,
            )
        except ThisIsATaskException as e:
            return await self.wait_for_task(e.response, e.args)

    async def wait_for_task(self, response: httpx.Response, args) -> httpx.Response:
        message = response.json()
        task_id = message["task_id"]
        status_location = response.headers.get("location")
        seconds_passed = 0
        while message["status"] not in {"completed", "failed"}:
            await asyncio.sleep(1)
            message = (
                await self.get(f"{self.endpoint}/{status_location}", absolute_url=True)
            ).json()
            seconds_passed += 1

            if seconds_passed > _TASK_TIMEOUT:
                raise Exception(f"Task {task_id} timed out. last status: {message}")

        if message["status"] == "failed":
            raise ApiServerError(f"Task {task_id} failed: {message}")

        result_url = message["result"]["content"]["url"]
        response = await self.get(f"{self.endpoint}/{result_url}", absolute_url=True)
        handle_response(response, args)
        return response

    @staticmethod
    def raise_for_status(fn):  # noqa: ANN202, ANN001
        @functools.wraps(fn)
        async def wrapped(*args, **kwargs):  # noqa: ANN202, ANN002, ANN003
            response = None
            try:
                response = await fn(
                    *args,
                    timeout=_DEFAULT_TIMEOUT,
                    **kwargs,
                )  # typing: ignore
            finally:
                handle_response(response, args)

            if response is not None and response.status_code == HTTPStatus.ACCEPTED:
                # this is a task that is being processed
                raise ThisIsATaskException(response, args)

            return response

        return wrapped


def handle_response(response: httpx.Response, args):
    if response is not None and response.status_code != HTTPStatus.OK:
        if response.headers.get("content-type") == "application/json":
            content_json = json.loads(response.content)
        else:
            content_json = {"detail": response.content}

        if response.status_code in _SERVER_ERROR_CODES:
            msg = (
                "An error occurred on the server side.",
                "",
                f"Status Code: {response.status_code}",
                os.linesep.join([f"{k}: {v}" for k, v in content_json.items()]),
            )  # type: ignore
            raise ApiServerError(os.linesep.join(msg))
        elif response.status_code in _CLIENT_ERROR_CODES:
            msg = (
                "A client-side error occurred. Please review the request and ",
                "try again.",
                f"Request ID: {response.headers.get('X-request-id')}",
                f"Arguments: {', '.join(map(str, args))}",
                f"Status Code: {response.status_code}",
                os.linesep.join([f"{k}: {v}" for k, v in content_json.items()]),
            )  # type: ignore
            raise ApiClientError(os.linesep.join(msg))
        else:
            response.raise_for_status()

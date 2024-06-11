from os import getenv
from time import time
from typing import Any, Dict, Optional, Union

import jwt
from galileo_core.helpers.execution import async_run

from galileo_observe.constants.routes import Routes
from galileo_observe.schema.transaction import TransactionRecordBatch
from galileo_observe.utils import __version__ as client_version
from galileo_observe.utils.request import HttpHeaders, make_request


class ApiClient:
    def __init__(self, project_name: str):
        self.project_id = None
        self.api_url = self.get_api_url()
        if self.healthcheck():
            self.token = self.get_token()
            try:
                project = self.get_project_by_name(project_name)
                if project["type"] not in ["llm_monitor", "galileo_observe"]:
                    raise Exception(
                        f"Project {project_name} is not a Galileo Observe project"
                    )
                self.project_id = project["id"]
            except Exception as e:
                if "not found" in str(e):
                    self.project_id = self.create_project(project_name)["id"]
                    print(f"🚀 Creating new project... project {project_name} created!")
                else:
                    raise e

    def get_api_url(self) -> str:
        console_url = getenv("GALILEO_CONSOLE_URL")
        if console_url is None:
            raise Exception("GALILEO_CONSOLE_URL must be set")
        if any(map(console_url.__contains__, ["localhost", "127.0.0.1"])):
            api_url = "http://localhost:8088"
        else:
            api_url = console_url.replace("console", "api")
        return api_url

    def get_token(self) -> str:
        api_key = getenv("GALILEO_API_KEY")
        if api_key:
            return self.api_key_login(api_key).get("access_token", "")

        username = getenv("GALILEO_USERNAME")
        password = getenv("GALILEO_PASSWORD")
        if username and password:
            return self.username_login(username, password).get("access_token", "")

        raise Exception(
            "GALILEO_API_KEY or GALILEO_USERNAME and GALILEO_PASSWORD must be set"
        )

    def healthcheck(self) -> bool:
        async_run(
            make_request("get", base_url=self.base_url, endpoint=Routes.healthcheck)
        )
        return True

    def username_login(self, username: str, password: str) -> Dict[str, str]:
        return async_run(
            make_request(
                "post",
                base_url=self.base_url,
                endpoint=Routes.login,
                data={
                    "username": username,
                    "password": password,
                    "auth_method": "email",
                },
            )
        )

    def api_key_login(self, api_key: str) -> Dict[str, str]:
        return async_run(
            make_request(
                "post",
                base_url=self.base_url,
                endpoint=Routes.api_key_login,
                body={
                    "api_key": api_key,
                },
            )
        )

    @property
    def base_url(self) -> str:
        return self.api_url

    @property
    def auth_header(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

    def _make_request(
        self,
        request_method: str,
        endpoint: str,
        body: Optional[Dict] = None,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        params: Optional[Dict] = None,
        timeout: Union[int, None] = None,
        json_request_only: bool = False,
    ) -> Any:
        # Check to see if our token is expired before making a request
        # and refresh token if it's expired
        if endpoint not in [Routes.login, Routes.api_key_login] and self.token:
            claims = jwt.decode(self.token, options={"verify_signature": False})
            if claims.get("exp", 0) < time():
                self.token = self.get_token()

        if json_request_only:
            content_headers = HttpHeaders.accept_json()
        else:
            content_headers = HttpHeaders.json()
        headers = {**self.auth_header, **content_headers}
        return async_run(
            make_request(
                request_method=request_method,
                base_url=self.base_url,
                endpoint=endpoint,
                body=body,
                data=data,
                files=files,
                params=params,
                headers=headers,
                timeout=timeout,
            )
        )

    async def _make_async_request(
        self,
        request_method: str,
        endpoint: str,
        body: Optional[Dict] = None,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        params: Optional[Dict] = None,
        timeout: Union[int, None] = None,
        json_request_only: bool = False,
    ) -> Any:
        # Check to see if our token is expired before making a request
        # and refresh token if it's expired
        if endpoint not in [Routes.login, Routes.api_key_login] and self.token:
            claims = jwt.decode(self.token, options={"verify_signature": False})
            if claims.get("exp", 0) < time():
                self.token = self.get_token()

        if json_request_only:
            content_headers = HttpHeaders.accept_json()
        else:
            content_headers = HttpHeaders.json()
        headers = {**self.auth_header, **content_headers}
        await make_request(
            request_method=request_method,
            base_url=self.base_url,
            endpoint=endpoint,
            body=body,
            data=data,
            files=files,
            params=params,
            headers=headers,
            timeout=timeout,
        )

    async def ingest_batch(
        self, transaction_batch: TransactionRecordBatch
    ) -> Dict[str, str]:
        transaction_batch.client_version = client_version
        return await self._make_async_request(
            "post",
            endpoint=Routes.ingest.format(project_id=self.project_id),
            body=transaction_batch.model_dump(),
        )

    def get_project_by_name(self, project_name: str) -> Any:
        projects = self._make_request(
            "get",
            endpoint=Routes.projects,
            params={"project_name": project_name},
        )
        if len(projects) < 1:
            raise Exception(f"Galileo project {project_name} not found")
        return projects[0]

    def create_project(self, project_name: str) -> Dict[str, str]:
        return self._make_request(
            "post",
            endpoint=Routes.projects,
            body={"name": project_name, "type": "llm_monitor"},
        )

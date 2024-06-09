import requests
from urllib.parse import urljoin
import json
from requests.adapters import HTTPAdapter, Retry
from typing import TypedDict
import uuid
import websocket
from typing import List,Union
from .message import MessageChannel,MessageResult
from .error import UnauthorizedError,JupterAPIError

def build_retryable_request(max_retries: int = 2) -> requests.Session:
    """ build retryable http request object """
    session = requests.Session()
    retries = Retry(total=max_retries, backoff_factor=0.1)
    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


class KernelInfo(TypedDict):
    id: str
    name: str
    last_activity: str
    connections: int
    execution_state: str

class SessionInfo(TypedDict):
    id: str
    path: str
    name: str
    type: str
    kernel: KernelInfo


class JupterGatewayClient:
    def __init__(self,server_host: str, server_port: int , auth_token: str, request_kwargs: dict = None, max_request_retries: int = 2, kernel_name: str = ""):
        self.server_host = server_host
        self.server_port = server_port
        self.request_kwargs = request_kwargs or {}
        if auth_token:
            self.headers = {"Authorization": f"token {auth_token}"}
        else:
            self.headers = {}
        self.session = build_retryable_request(max_retries=max_request_retries)
        self.base_http_addr = f"http://{server_host}:{server_port}"
        self.base_ws_addr = f"ws://{server_host}:{server_port}"
        self.kernel_name = kernel_name or self.get_kernel_specs()["default"]

    def request(self, method, url, **kwargs) -> requests.Response:
        """ reqeust to jupyter gateway server """
        resp = self.session.request(url=url, method=method,**kwargs)
        content = resp.text
        if 'Unauthorized' in content:
            raise UnauthorizedError(content)
        if "reason" in content and "message" in content:
            raise JupterAPIError(content)
        return resp

    def get_kernel_specs(self):
        """ Get kernel specs """
        method = "GET"
        url = urljoin(self.base_http_addr,"/api/kernelspecs")
        kwargs = self.request_kwargs.copy()
        headers = self.headers.copy()
        resp = self.request(url=url,
                            method=method,
                            headers=headers,
                            **kwargs)
        return resp.json()

    def get_kernels(self,kernel_id:str=None) -> Union[List[KernelInfo],KernelInfo]:
        """ get runnnig kernel list

        Returns:
            >>> resp.json()
            >>> {
            ... "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            ... "name": "string",
            ... "last_activity": "string",
            ... "connections": 0,
            ... "execution_state": "string"
            ... }
        """
        method = "GET"
        base_uri = "/api/kernels"
        if kernel_id:
            uri = f"{base_uri}/{kernel_id}"
        else:
            uri = base_uri
        url = urljoin(self.base_http_addr, uri)
        kwargs = self.request_kwargs.copy()
        resp = self.request(url=url,
                            method=method,
                            headers=self.headers.copy(),
                            **kwargs)
        return resp.json()


    def create_kernel(self,name: str = None) -> KernelInfo:
        """ Start a kernel and return the uuid

        Examples:
            >>> resp.json()
            >>> {
            ...   "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            ...   "name": "string",
            ...   "last_activity": "string",
            ...   "connections": 0,
            ...    "execution_state": "string"
            ... }
        """
        if not name:
            name = self.kernel_name
        method = "POST"
        url = urljoin(self.base_http_addr, "/api/kernels")
        kwargs = self.request_kwargs.copy()
        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"
        data = json.dumps({"name": f"{name}"})
        resp = self.request(url=url,
                            method=method,
                            data=data,
                            headers=headers,
                            **kwargs)
        return resp.json()



    def get_sessions(self,session_id:str = "") -> Union[List[SessionInfo],SessionInfo]:
        """ get avaiable sessions list """
        method = "GET"
        base_uri = "/api/sessions"
        # todo /api/sessions/{session_id} hace some problem
        url = urljoin(self.base_http_addr, base_uri)
        kwargs = self.request_kwargs.copy()
        resp = self.request(url=url,
                            method=method,
                            headers=self.headers.copy(),
                            **kwargs)
        sessions = resp.json()
        if session_id:
            for session in sessions:
                if session["id"] == session_id:
                    return session
        return sessions


    def create_session(self,session_type:str = "", path: str = "") -> SessionInfo:
        """ create session """
        if not path:
            path = f"/{uuid.uuid4().hex}"
        method = "POST"
        url = urljoin(self.base_http_addr, "/api/sessions")
        kwargs = self.request_kwargs.copy()
        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"
        obj =  {
          "path": path,
          "type": session_type,
        }
        data = json.dumps(obj)
        resp = self.request(url=url,
                            method=method,
                            data=data,
                            headers=headers,
                            **kwargs)
        return resp.json()


    def upgrade_websocket_channel(self,kernel_id: str,session_id: str = "") -> MessageChannel:
        """ upgrad to websocket channel """
        uri = f"/api/kernels/{kernel_id}/channels"
        url = urljoin(self.base_ws_addr, uri)
        ws = websocket.create_connection(url, header=self.headers.copy())

        if not session_id:
            session_id = uuid.uuid4().hex
        return MessageChannel(
            ws=ws,
            session_id=session_id,
        )


    def create_execute_channel(self) -> MessageChannel:
        """ create execute channel """
        session_info = self.create_session()
        kernel_id = session_info["kernel"]["id"]
        session_id = session_info["id"]
        channel = self.upgrade_websocket_channel(
            kernel_id=kernel_id,
            session_id=session_id
        )
        return channel


    def code_interpreter(self,code: str) -> MessageResult:
        """
        coder interpreter

        Args:
            code: Code that needs to be executed

        Returns:
            MessageResult：jupyter message

        """
        execute_channel = self.create_execute_channel()
        execute_result = execute_channel.execute_request(code=code)
        return execute_result






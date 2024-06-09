from pydantic import BaseModel,ConfigDict
from typing import Dict,List,Optional
from enum import Enum

# ref: https://jupyter-client.readthedocs.io/en/stable/messaging.html

class ReplyStatus(Enum):
    ok = "ok"
    error = "error"
    abort = "abort"

class KernelStatus(Enum):
    busy = "busy"
    idle = "idle"
    starting = "starting"


class RequestContent(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

class ReplyContent(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    status: ReplyStatus

    # status
    ename: Optional[str] = None
    evalue: Optional[str] = None
    traceback: Optional[List[str]] = None

class DataContent(BaseModel): pass


class ExecuteRequest(RequestContent):
    code: str
    silent: bool
    store_history: bool
    user_expressions: Dict
    allow_stdin: bool
    stop_on_error: bool

class ExecuteReply(ReplyContent):
    execution_count: int
    payload: List[Dict] = []
    user_expressions: Dict = {}


class ExecuteResult(DataContent):
    execution_count: int
    data: dict
    metadata: dict


class InspectRequest(RequestContent):
    code: str
    cursor_pos: int
    detail_level: int # 0 or q

class InspectReply(ReplyContent):
    found: bool
    data: dict
    metadata: dict

class CompleteRequest(RequestContent):
    code: str
    cursor_pos: int

class CompleteReply(ReplyContent):
    matches: list
    cursor_start: int
    cursor_end: int
    metadata: dict

class HistoryRequest(RequestContent):
    output: bool
    raw: bool
    hist_access_type: str
    session: int
    start: int
    stop: int
    n: int
    pattern: str
    unique: bool

class HistoryReply(ReplyContent):
    history: list


class IsCompleteRequest(RequestContent):
    code: str


class IsCompleteReply(ReplyContent):
    indent: str

class CommInfoRequest(RequestContent):
    target_name: str


class CommInfoReply(ReplyContent):
    comms: Dict


class KernelInfoRequest(RequestContent): pass

class KernelInfoReply(ReplyContent):
    protocol_version: str # 协议版本
    implementation: str
    implementation_version: str
    language_info: Dict # 协议语言的版本信息
    banner: str
    debugger: bool
    help_links: List


class ShutdownRequest(RequestContent):
    restart: bool # 是否重启


class ShutdownReply(ReplyContent):
    restart: bool


class InterruptRequest(RequestContent): pass
class InterruptReply(ReplyContent): pass
class DebugRequest(RequestContent): pass
class DebugReply(ReplyContent): pass

class Streams(DataContent):
    name: str # stdout stderror
    text: str

class DisplayData(DataContent):
    data: dict
    metadata: dict
    transient: dict


class UpdateDisplayData(DataContent):
    data: dict
    metadata: dict
    transient: dict


class ExecuteInput(DataContent):
    code: str
    execution_count: int


class Error(DataContent): pass


class Status(DataContent):
    model_config = ConfigDict(use_enum_values=True)
    execution_state: KernelStatus


class ClearOutput(RequestContent):
    wait: bool

class DebugEvent(DataContent): pass


class InputRequest(RequestContent):
    prompt: str
    password: bool

class InputReply(ReplyContent):
    value: str


class CommMsg(DataContent):
    comm_id: str
    data: dict


class CommClose(DataContent):
    comm_id: str
    data: dict


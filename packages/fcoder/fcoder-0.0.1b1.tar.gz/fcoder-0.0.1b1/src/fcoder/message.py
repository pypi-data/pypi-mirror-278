from .content import *
from pydantic import BaseModel,ConfigDict
from enum import Enum
from typing import Any,Union
from datetime import datetime
import uuid
from websocket import WebSocket
import json


class MessageType(Enum):
    """
    Message type

    References:
        1. https://jupyter-client.readthedocs.io/en/stable/messaging.html
    """
    execute_request = "execute_request"
    execute_reply = "execute_reply"
    inspect_request = "inspect_request"
    inspect_reply = "inspect_reply"
    complete_request = "complete_request"
    complete_reply = "complete_reply"
    history_request = "history_request"
    history_reply = "history_reply"
    is_complete_request = "is_complete_request"
    is_complete_reply = "is_complete_reply"

    # Deprecated since version 5.1
    # connect_request = "connect_request"
    # connect_reply = "connect_reply"

    comm_info_request = "comm_info_request"
    comm_info_reply = "comm_info_reply"
    kernel_info_request = "kernel_info_request"
    kernel_info_reply = "kernel_info_reply"
    shutdown_request = "shutdown_request"
    shutdown_reply = "shutdown_reply"
    interrupt_request = "interrupt_request"
    interrupt_reply = "interrupt_reply"
    debug_request = "debug_request"
    debug_reply = "debug_reply"
    stream = "stream"
    display_data = "display_data"
    update_display_data = "update_display_data"
    execute_input = "execute_input"
    execute_result = "execute_result"
    error = "error"
    status = "status"
    clear_output = "clear_output"
    debug_event = "debug_event"
    input_request = "input_request"
    input_reply = "input_reply"
    comm_msg = "comm_msg"
    comm_close = "comm_close"



class ChannelType(Enum):
    """ message channel type """
    shell = "shell"
    iopub = "iopub"
    stdin = "stdin"
    control = "control"
    heartbeat = "heartbeat"


class MessageHeader(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    msg_id: str # unique uuid
    session: str # unique uuid
    msg_type: MessageType
    username: str = "general"
    version: str = "5.0" #
    date: str = None

    def model_post_init(self, __context: Any) -> None:
        # 自动生成时间消息
        if not self.date:
            self.date = datetime.now().isoformat()


class CommMessage(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    # ref: https://jupyter-client.readthedocs.io/en/stable/messaging.html
    content: Dict
    header: MessageHeader
    parent_header: Optional[MessageHeader] = None
    channel: ChannelType
    metadata: Dict = {}
    buffers: list = []


class DisplayMimeType(Enum):
    # ref: https://jupyterlab.readthedocs.io/en/stable/user/file_formats.html
    text_plain = "text/plain"
    # Markdown
    text_markdown = "text/markdown"
    # Images
    image_bmp = "image/bmp"
    image_gif = "image/gif"
    image_jpeg = "image/jpeg"
    image_png = "image/png"
    image_svg_xml = "image/svg+xml"
    # JSON
    application_json = "application/json"
    # HTML
    text_html = "text/html"
    # LaTeX
    text_latex = "text/latex"
    # PDF
    application_pdf = "application/pdf"
    # Vega
    application_vega_json = "application/vnd.vega.v5+json"
    # Vega-Lite
    application_vega_lite_json = "application/vnd.vegalite.v3+json"


class ErrorTrace(BaseModel):
    model_config = ConfigDict(extra="ignore")
    ename: str
    evalue: str
    traceback: list[str]




class MessageResultStatus(Enum):
    ok = ReplyStatus.ok.value
    error = ReplyStatus.error.value
    abort = ReplyStatus.abort.value
    failed = "failed"

class MessageResult(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    status: MessageResultStatus
    output: List[Dict[str,str]] = [] # 输出结果
    error_trace: Optional[ErrorTrace] = None
    message: str = ""


class MessageChannel:
    def __init__(self,ws: WebSocket, session_id: str):
        self.websocket = ws
        self.session = session_id

    def build_message(self,
                      content: Union[Dict,BaseModel],
                      msg_type: MessageType,
                      channel: ChannelType,
                      msg_id: str = "",
                      parent_header: Optional[MessageHeader] = None,
                      metadata: dict = None,
                      buffers: list = None,
                      ):
        """ build message """
        if isinstance(content,BaseModel):
            content = content.model_dump()
        if not metadata: metadata = {}
        if not buffers: buffers = []
        if not msg_id:
            msg_id = uuid.uuid4().hex
        message_header = MessageHeader(msg_id=msg_id, session=self.session, msg_type=msg_type)
        message = CommMessage(
            header=message_header,
            parent_header=parent_header,
            content=content,
            channel=channel,
            metadata=metadata,
            buffers=buffers
        )
        return message

    def send_message(self,message: CommMessage):
        """ send message """
        self.websocket.send_text(message.model_dump_json())

    def recv_message(self) -> CommMessage:
        """ receive message """
        data = json.loads(self.websocket.recv())
        message = CommMessage(**data)
        return message


    def execute_reply(self,message_id: str) -> MessageResult:
        """ execute reply """
        result = MessageResult(status=MessageResultStatus.failed)
        while True:
            data = json.loads(self.websocket.recv())
            message = CommMessage(**data)
            if message.parent_header.msg_id != message_id:
                continue
            match message.header.msg_type:
                case MessageType.execute_input.value: pass
                case MessageType.stream.value:
                    content = Streams(**message.content)
                    # 结果
                    result.output.append({
                        DisplayMimeType.text_plain.value: content.text
                    })
                case MessageType.display_data.value:
                    content = DisplayData(**message.content)
                    result.output.append(content.data)

                case MessageType.execute_result.value:
                    content = ExecuteResult(**message.content)
                    result.output.append(content.data)

                case MessageType.execute_reply.value:
                    content = ExecuteReply(**message.content)
                    result.status = content.status
                    if result.status == ReplyStatus.error.value:
                        result.error_trace = ErrorTrace(**message.content)
                    return result
                case _:
                    continue
        result.message = "No reply message received."
        return result

    def execute_request(self,code: str,
                silent: bool = False,
                store_history:bool = True,
                user_expressions: Dict = None,
                allow_stdin: bool = False,
                stop_on_error: bool=True
        ) -> MessageResult:
        """
        execute request

        Args:
            code:
            silent:
            store_history:
            user_expressions:
            allow_stdin:
            stop_on_error:

        Returns:

        """
        if not user_expressions: user_expressions = {}
        content = ExecuteRequest(
            code=code,
            silent=silent,
            store_history=store_history,
            user_expressions=user_expressions,
            allow_stdin=allow_stdin,
            stop_on_error=stop_on_error
        )
        message = self.build_message(
            content=content,
            msg_type=MessageType.execute_request,
            channel=ChannelType.shell
        )

        self.send_message(message)
        result = self.execute_reply(message_id=message.header.msg_id)
        return result


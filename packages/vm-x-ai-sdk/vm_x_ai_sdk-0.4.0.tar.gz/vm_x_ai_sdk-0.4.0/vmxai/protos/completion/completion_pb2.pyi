from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RequestTools(_message.Message):
    __slots__ = ("type", "function")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    type: str
    function: RequestToolFunction
    def __init__(self, type: _Optional[str] = ..., function: _Optional[_Union[RequestToolFunction, _Mapping]] = ...) -> None: ...

class RequestToolFunction(_message.Message):
    __slots__ = ("name", "description", "parameters")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    parameters: _struct_pb2.Struct
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., parameters: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class RequestToolChoice(_message.Message):
    __slots__ = ("auto", "none", "tool")
    AUTO_FIELD_NUMBER: _ClassVar[int]
    NONE_FIELD_NUMBER: _ClassVar[int]
    TOOL_FIELD_NUMBER: _ClassVar[int]
    auto: bool
    none: bool
    tool: RequestToolChoiceItem
    def __init__(self, auto: bool = ..., none: bool = ..., tool: _Optional[_Union[RequestToolChoiceItem, _Mapping]] = ...) -> None: ...

class RequestToolChoiceItem(_message.Message):
    __slots__ = ("type", "function")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    type: str
    function: RequestToolChoiceFunction
    def __init__(self, type: _Optional[str] = ..., function: _Optional[_Union[RequestToolChoiceFunction, _Mapping]] = ...) -> None: ...

class RequestToolChoiceFunction(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class RequestMessage(_message.Message):
    __slots__ = ("name", "role", "content", "tool_calls", "tool_call_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    TOOL_CALLS_FIELD_NUMBER: _ClassVar[int]
    TOOL_CALL_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    role: str
    content: str
    tool_calls: _containers.RepeatedCompositeFieldContainer[RequestMessageToolCall]
    tool_call_id: str
    def __init__(self, name: _Optional[str] = ..., role: _Optional[str] = ..., content: _Optional[str] = ..., tool_calls: _Optional[_Iterable[_Union[RequestMessageToolCall, _Mapping]]] = ..., tool_call_id: _Optional[str] = ...) -> None: ...

class RequestMessageToolCall(_message.Message):
    __slots__ = ("id", "type", "function")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    function: RequestMessageToolCallFunction
    def __init__(self, id: _Optional[str] = ..., type: _Optional[str] = ..., function: _Optional[_Union[RequestMessageToolCallFunction, _Mapping]] = ...) -> None: ...

class RequestMessageToolCallFunction(_message.Message):
    __slots__ = ("name", "arguments")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    name: str
    arguments: str
    def __init__(self, name: _Optional[str] = ..., arguments: _Optional[str] = ...) -> None: ...

class CompletionRequest(_message.Message):
    __slots__ = ("resource", "workload", "stream", "messages", "tools", "tool_choice", "config")
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    WORKLOAD_FIELD_NUMBER: _ClassVar[int]
    STREAM_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    TOOLS_FIELD_NUMBER: _ClassVar[int]
    TOOL_CHOICE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    resource: str
    workload: str
    stream: bool
    messages: _containers.RepeatedCompositeFieldContainer[RequestMessage]
    tools: _containers.RepeatedCompositeFieldContainer[RequestTools]
    tool_choice: RequestToolChoice
    config: _struct_pb2.Struct
    def __init__(self, resource: _Optional[str] = ..., workload: _Optional[str] = ..., stream: bool = ..., messages: _Optional[_Iterable[_Union[RequestMessage, _Mapping]]] = ..., tools: _Optional[_Iterable[_Union[RequestTools, _Mapping]]] = ..., tool_choice: _Optional[_Union[RequestToolChoice, _Mapping]] = ..., config: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class CompletionResponse(_message.Message):
    __slots__ = ("id", "message", "role", "tool_calls", "usage", "response_timestamp")
    ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    TOOL_CALLS_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    id: str
    message: str
    role: str
    tool_calls: _containers.RepeatedCompositeFieldContainer[RequestMessageToolCall]
    usage: CompletionUsage
    response_timestamp: int
    def __init__(self, id: _Optional[str] = ..., message: _Optional[str] = ..., role: _Optional[str] = ..., tool_calls: _Optional[_Iterable[_Union[RequestMessageToolCall, _Mapping]]] = ..., usage: _Optional[_Union[CompletionUsage, _Mapping]] = ..., response_timestamp: _Optional[int] = ...) -> None: ...

class CompletionUsage(_message.Message):
    __slots__ = ("prompt", "completion", "total")
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    prompt: int
    completion: int
    total: int
    def __init__(self, prompt: _Optional[int] = ..., completion: _Optional[int] = ..., total: _Optional[int] = ...) -> None: ...

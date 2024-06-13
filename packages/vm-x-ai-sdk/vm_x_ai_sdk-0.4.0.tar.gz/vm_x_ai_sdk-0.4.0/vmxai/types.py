from dataclasses import dataclass, field
from typing import Literal, Optional, Union

from vmxai.protos.completion.completion_pb2 import RequestMessageToolCall, RequestToolChoiceItem, RequestTools


@dataclass
class RequestMessage:
    role: Literal["system", "user", "assistant", "tool"]
    name: Optional[str] = field(default=None)
    content: Optional[str] = field(default=None)
    tool_call_id: Optional[str] = field(default=None)
    tool_calls: Optional[list[RequestMessageToolCall]] = field(default_factory=list)


@dataclass
class CompletionRequest:
    resource: str
    workload: str
    tools: Optional[list[RequestTools]] = field(default_factory=list)
    tool_choice: Optional[Union[Literal["auto", "none"], RequestToolChoiceItem]] = "auto"
    config: Optional[dict] = field(default_factory=dict)
    messages: list[RequestMessage] = field(default_factory=list)

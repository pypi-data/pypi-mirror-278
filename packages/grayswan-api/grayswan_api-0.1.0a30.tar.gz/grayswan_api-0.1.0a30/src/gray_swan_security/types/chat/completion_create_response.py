# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = [
    "CompletionCreateResponse",
    "CreateChatCompletionResponse",
    "CreateChatCompletionResponseChoice",
    "CreateChatCompletionResponseChoiceMessage",
    "CreateChatCompletionResponseChoiceMessageToolCall",
    "CreateChatCompletionResponseChoiceMessageToolCallFunction",
    "CreateChatCompletionResponseUsage",
    "CreateChatCompletionStreamResponse",
    "CreateChatCompletionStreamResponseChoice",
    "CreateChatCompletionStreamResponseChoiceDelta",
    "CreateChatCompletionStreamResponseChoiceDeltaToolCall",
    "CreateChatCompletionStreamResponseChoiceDeltaToolCallFunction",
]


class CreateChatCompletionResponseChoiceMessageToolCallFunction(BaseModel):
    arguments: str

    name: str


class CreateChatCompletionResponseChoiceMessageToolCall(BaseModel):
    id: str

    function: CreateChatCompletionResponseChoiceMessageToolCallFunction

    type: Literal["function"]


class CreateChatCompletionResponseChoiceMessage(BaseModel):
    role: Literal["assistant"]

    content: Optional[str] = None

    tool_calls: Optional[List[CreateChatCompletionResponseChoiceMessageToolCall]] = None


class CreateChatCompletionResponseChoice(BaseModel):
    finish_reason: Literal["stop", "length", "content_filter", "tool_calls"]

    index: int

    message: CreateChatCompletionResponseChoiceMessage

    logprobs: Optional[str] = None


class CreateChatCompletionResponseUsage(BaseModel):
    completion_tokens: int

    prompt_tokens: int

    total_tokens: int


class CreateChatCompletionResponse(BaseModel):
    id: str

    choices: List[CreateChatCompletionResponseChoice]

    created: int

    model: str

    object: Literal["chat.completion"]

    system_fingerprint: Optional[str] = None

    usage: Optional[CreateChatCompletionResponseUsage] = None


class CreateChatCompletionStreamResponseChoiceDeltaToolCallFunction(BaseModel):
    arguments: Optional[str] = None

    name: Optional[str] = None


class CreateChatCompletionStreamResponseChoiceDeltaToolCall(BaseModel):
    index: int

    id: Optional[str] = None

    function: Optional[CreateChatCompletionStreamResponseChoiceDeltaToolCallFunction] = None

    type: Optional[Literal["function"]] = None


class CreateChatCompletionStreamResponseChoiceDelta(BaseModel):
    content: Optional[str] = None

    role: Optional[Literal["system", "user", "assistant", "tool"]] = None

    tool_calls: Optional[List[CreateChatCompletionStreamResponseChoiceDeltaToolCall]] = None


class CreateChatCompletionStreamResponseChoice(BaseModel):
    delta: CreateChatCompletionStreamResponseChoiceDelta

    index: int

    finish_reason: Optional[Literal["stop", "length", "content_filter", "tool_calls"]] = None


class CreateChatCompletionStreamResponse(BaseModel):
    id: str

    choices: List[CreateChatCompletionStreamResponseChoice]

    created: int

    model: str

    object: Literal["chat.completion.chunk"]

    system_fingerprint: Optional[str] = None


CompletionCreateResponse = Union[CreateChatCompletionResponse, CreateChatCompletionStreamResponse]

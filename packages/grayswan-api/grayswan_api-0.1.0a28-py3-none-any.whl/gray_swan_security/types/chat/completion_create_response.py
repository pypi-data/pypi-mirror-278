# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .chat_completion_choice import ChatCompletionChoice
from .chat_completion_stream_choice import ChatCompletionStreamChoice

__all__ = [
    "CompletionCreateResponse",
    "CreateChatCompletionResponse",
    "CreateChatCompletionResponseUsage",
    "CreateChatCompletionStreamResponse",
]


class CreateChatCompletionResponseUsage(BaseModel):
    completion_tokens: int

    prompt_tokens: int

    total_tokens: int


class CreateChatCompletionResponse(BaseModel):
    id: str

    choices: List[ChatCompletionChoice]

    created: int

    model: str

    object: Literal["chat.completion"]

    system_fingerprint: Optional[str] = None

    usage: Optional[CreateChatCompletionResponseUsage] = None


class CreateChatCompletionStreamResponse(BaseModel):
    id: str

    choices: List[ChatCompletionStreamChoice]

    created: int

    model: str

    object: Literal["chat.completion.chunk"]

    system_fingerprint: Optional[str] = None


CompletionCreateResponse = Union[CreateChatCompletionResponse, CreateChatCompletionStreamResponse]

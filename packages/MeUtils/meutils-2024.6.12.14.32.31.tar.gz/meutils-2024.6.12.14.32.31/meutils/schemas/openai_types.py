#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_types
# @Time         : 2024/6/7 17:30
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 
import shortuuid
from meutils.pipe import *

from openai.types.chat import ChatCompletion as _ChatCompletion, ChatCompletionChunk as _ChatCompletionChunk
from openai.types.chat.chat_completion import Choice as _Choice, ChatCompletionMessage as _ChatCompletionMessage, \
    CompletionUsage as _CompletionUsage
from openai.types.chat.chat_completion_chunk import Choice as _ChunkChoice, ChoiceDelta


class CompletionUsage(_CompletionUsage):
    prompt_tokens: int = 1
    completion_tokens: int = 1
    total_tokens: int = 1


class ChatCompletionMessage(_ChatCompletionMessage):
    role: Literal["assistant"] = "assistant"
    """The role of the author of this message."""


class Choice(_Choice):
    index: int = 0
    finish_reason: Literal["stop", "length", "tool_calls", "content_filter", "function_call"] = None


class ChatCompletion(_ChatCompletion):
    id: str = Field(default_factory=shortuuid.random)
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str = ""
    object: str = "chat.completion"
    usage: CompletionUsage = CompletionUsage()


class ChunkChoice(_ChunkChoice):
    index: int = 0


class ChatCompletionChunk(_ChatCompletionChunk):
    id: str = Field(default_factory=shortuuid.random)
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str = ""
    object: str = "chat.completion.chunk"


chat_completion = ChatCompletion(
    choices=[Choice(message=ChatCompletionMessage(content=""))]
)
chat_completion_chunk = ChatCompletionChunk(
    choices=[ChunkChoice(delta=ChoiceDelta(content=""))]
)
chat_completion_chunk_stop = ChatCompletionChunk(
    choices=[ChunkChoice(delta=ChoiceDelta(content=""), finish_reason="stop")]
)

# chat_completion.choices[0].message.content = "*"
# chat_completion_chunk.choices[0].delta.content = "*"

if __name__ == '__main__':
    # print(ChatCompletion(choices=[Choice(message=ChatCompletionMessage(content="ChatCompletion"))]))
    # print(ChatCompletionChunk(choices=[ChunkChoice(delta=ChoiceDelta(content="ChatCompletionChunk"))]))
    #
    print(chat_completion)
    print(chat_completion_chunk)
    print(chat_completion_chunk_stop)

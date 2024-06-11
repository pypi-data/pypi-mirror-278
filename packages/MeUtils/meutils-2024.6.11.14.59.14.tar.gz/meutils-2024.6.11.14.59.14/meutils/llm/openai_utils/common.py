#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : commom
# @Time         : 2024/5/30 11:20
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import time

import shortuuid
import tiktoken

from meutils.pipe import *
from meutils.async_utils import achain

from openai import AsyncOpenAI, OpenAI, AsyncStream

from meutils.queues.smooth_queue import SmoothQueue
from meutils.schemas.openai_types import ChatCompletion, ChatCompletionChunk, CompletionUsage
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, chat_completion_chunk_stop  # todo

token_encoder = tiktoken.get_encoding('cl100k_base')


def ppu(model='ppu', api_key: Optional[str] = None):
    client = OpenAI(api_key=api_key)
    return client.chat.completions.create(messages=[{'role': 'user', 'content': 'hi'}], model=model)


async def appu(model='ppu', api_key: Optional[str] = None):
    client = AsyncOpenAI(api_key=api_key)
    return await client.chat.completions.create(messages=[{'role': 'user', 'content': 'hi'}], model=model)


def create_chat_completion(
        completion: Union[str, ChatCompletion],
        redirect_model: str = '',

        alfa: float = 1,
        prompt_tokens: int = 1,
):
    if isinstance(completion, str):
        chat_completion.choices[0].message.content = completion

    if chat_completion.usage.total_tokens == 1:
        completion_tokens = int(alfa * len(token_encoder.encode(str(completion))))
        chat_completion.usage = CompletionUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens
        )

    chat_completion.model = redirect_model or chat_completion.model
    return chat_completion


async def create_chat_completion_chunk(
        completion_chunks: Union[
            Coroutine,
            AsyncStream[ChatCompletionChunk],
            Iterator[Union[str, ChatCompletionChunk]],
            AsyncIterator[Union[str, ChatCompletionChunk]]
        ],
        redirect_model: str = ''
):
    """
        async def main():
            data = {}
            _ = AsyncOpenAI().chat.completions.create(**data)
            async for i in create_chat_completion_chunk(_):
                print(i)
    :param completion_chunks:
    :param redirect_model:
    :return:
    """

    if isinstance(completion_chunks, Coroutine):
        completion_chunks = await completion_chunks

    async for completion_chunk in achain(completion_chunks):

        # logger.debug(completion_chunk)

        id = shortuuid.random()
        created = int(time.time())
        if isinstance(completion_chunk, str):
            chat_completion_chunk.id = id
            chat_completion_chunk.created = created
            chat_completion_chunk.choices[0].delta.content = completion_chunk
            chat_completion_chunk.model = redirect_model or chat_completion_chunk.model
            yield chat_completion_chunk.model_dump_json()
        else:
            completion_chunk.model = redirect_model or completion_chunk.model
            yield completion_chunk.model_dump_json()

    yield chat_completion_chunk_stop.model_dump_json()
    yield "[DONE]"  # 兼容标准格式


if __name__ == '__main__':
    # print(ppu())
    # print(appu())
    # print(arun(appu()))

    # print(create_chat_completion('hi'))
    print(create_chat_completion('hi', redirect_model='@@'))


    async def main():
        async for i in create_chat_completion_chunk(['hi', 'hi'], redirect_model='@@'):
            print(i)


    arun(main())

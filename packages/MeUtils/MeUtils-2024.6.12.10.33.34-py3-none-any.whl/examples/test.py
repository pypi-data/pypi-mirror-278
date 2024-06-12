#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : test
# @Time         : 2024/6/11 11:58
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import time
import typing

from meutils.pipe import *
from starlette.background import BackgroundTask as _BackgroundTask, BackgroundTasks as _BackgroundTasks
from asgiref.sync import async_to_sync


class BackgroundTask(_BackgroundTask):

    def call(self):
        async_to_sync(super().__call__)()


class BackgroundTasks(_BackgroundTasks):

    def call(self):
        async_to_sync(super().__call__)()


# def is_async_callable(obj: typing.Any) -> bool:
#     while isinstance(obj, functools.partial):
#         obj = obj.func
#
#     return asyncio.iscoroutinefunction(obj) or (
#             callable(obj) and asyncio.iscoroutinefunction(obj.__call__)
#     )


async def f(x):
    logger.debug(x)

    for i in range(100):
        logger.debug(i)
        await asyncio.sleep(1)


# def f(x):
#     logger.debug(x)
#
#     for i in range(100):
#         logger.debug(i)
#         time.sleep(1)


# BackgroundTask(f, x='xxxxxxxxxx').call()

bt = BackgroundTasks()
bt.add_task(f, x='xxxxxxxxxx')
bt.call()

while 1:
    pass

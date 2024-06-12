#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : check_token
# @Time         : 2024/5/9 15:41
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *

from fastapi import status
from fastapi import APIRouter, File, UploadFile, Query, Form, Response, Request

router = APIRouter()

# 从飞书获取tokens
# 遍历tokens
# 写入redis set

# import redis
#
# r = redis.Redis(host='localhost', port=6379, db=0)
# r.sadd('myset', 'value1')
# r.sadd('myset', 'value2')


# @router.get()


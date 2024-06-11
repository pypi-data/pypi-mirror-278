#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : task_types
# @Time         : 2024/5/31 15:47
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


class Task(BaseModel):
    task_id: Optional[str] = None
    data: Optional[dict] = None
    status: Optional[str] = None  # pending, running, success, failed
    metadata: Optional[dict] = None
    # {
    #     "description": "sentiment classification"
    # }


if __name__ == '__main__':
    print(Task(data=None))

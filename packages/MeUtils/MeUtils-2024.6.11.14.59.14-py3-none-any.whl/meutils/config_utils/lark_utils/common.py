#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2024/5/6 08:52
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from urllib.parse import urlparse, parse_qs


@lru_cache()
def get_app_access_token(ttl: Optional[int] = None):
    """
        get_app_access_token(ttl_fn(10))

    :param ttl:
    :return:
    """
    payload = {
        "app_id": os.getenv("FEISHU_APP_ID"),
        "app_secret": os.getenv("FEISHU_APP_SECRET")
    }
    response = httpx.post(
        "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal",
        json=payload,
        timeout=30,
    )

    # logger.debug(response.json())

    return response.json().get("app_access_token")


def get_spreadsheet_values(
        spreadsheet_token: Optional[str] = None,
        sheet_id: Optional[str] = None,
        feishu_url=None,
        to_dataframe: Optional[bool] = False
):
    if feishu_url and feishu_url.startswith("http"):
        parsed_url = urlparse(feishu_url)
        spreadsheet_token = parsed_url.path.split('/')[-1]
        sheet_id = parsed_url.query.split('=')[-1]

    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{sheet_id}"

    headers = {
        "Authorization": f"Bearer {get_app_access_token(ttl_fn(3600))}"
    }
    response = httpx.get(url, headers=headers, timeout=30)
    _ = response.json()
    return _ if not to_dataframe else pd.DataFrame(_.get('data').get('valueRange').get('values'))


def create_document(title: str = "一篇新文档🔥", folder_token: Optional[str] = None):
    payload = {
        "title": title,
        "folder_token": folder_token,
    }

    url = "https://open.feishu.cn/open-apis/docx/v1/documents"
    headers = {
        "Authorization": f"Bearer {get_app_access_token(ttl_fn(3600))}"
    }
    response = httpx.post(url, headers=headers, timeout=30, json=payload)
    return response.json()


def get_doc_raw_content(document_id: str = "BxlwdZhbyoyftZx7xFbcGCZ8nah"):
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/raw_content"
    headers = {
        "Authorization": f"Bearer {get_app_access_token(ttl_fn(3600))}"
    }
    response = httpx.get(url, headers=headers, timeout=30)
    return response.json()


if __name__ == '__main__':
    print(get_app_access_token())
    # print(get_spreadsheet_values("Qy6OszlkIhwjRatkaOecdZhOnmh", "0f8eb3"))
    # pprint(get_spreadsheet_values("Bmjtst2f6hfMqFttbhLcdfRJnNf", "Y9oalh"))
    # pd.DataFrame(
    #     get_spreadsheet_values("Bmjtst2f6hfMqFttbhLcdfRJnNf", "79272d").get('data').get('valueRange').get('values'))

    # print(get_doc_raw_content("TAEFdXmzyobvgUxKM3lcLfc2nxe"))
    # print(create_document())
    # "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=79272d"

    r = get_spreadsheet_values(feishu_url="https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=79272d",
                               to_dataframe=True)
    print(list(filter(None, r[0])))
    # print(get_spreadsheet_values("Bmjtst2f6hfMqFttbhLcdfRJnNf", "79272d"))

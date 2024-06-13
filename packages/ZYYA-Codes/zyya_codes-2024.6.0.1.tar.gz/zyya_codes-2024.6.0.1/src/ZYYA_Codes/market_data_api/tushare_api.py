# -*- coding: utf-8 -*-
"""
@Time ： 2023/9/16 22:15
@Auth ： Alan Gong
@File ：tushare_api.py
@IDE ：PyCharm
"""
import tushare
from ZYYA_Codes.utils import get_configs


def tushare_set_token(token):
    tushare.set_token(token)


def tushare_api():
    return tushare.pro_api(token=get_configs().get("tushare_token", {}).get("token", None))


tushare_pro_api = tushare_api()

__all__ = [
    "tushare_pro_api",
    "tushare_set_token"
]

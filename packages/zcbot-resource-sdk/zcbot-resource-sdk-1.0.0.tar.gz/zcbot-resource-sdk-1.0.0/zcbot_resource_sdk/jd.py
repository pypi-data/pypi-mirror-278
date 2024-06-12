import json
import logging
from typing import List, Optional
from zcbot_web_core.lib import time as time_lib
from zcbot_resource_sdk.common.model import ResCookie
from zcbot_resource_sdk.common.redis_client import SingletonRedis

LOGGER = logging.getLogger('京东')
rds = SingletonRedis(redis_uri=None, redis_db=None)


def get_ck_list(origin_key_list: List[str]) -> List[str]:
    """

    :param origin_key_list: redis键
    :return: List[cookie-pin]
    """
    temp = []
    for key in origin_key_list:
        cookie_list = key.split(":")
        temp.append(cookie_list[-1])
    return temp


def __is_banded(cookie_pin: str):
    """某个cookie是否被禁用"""
    return rds.client.sismember("res:jd:banded", cookie_pin)


def __banded_cookie(cookie_pin: str):
    """禁用某个cookie"""
    rds.client.sadd("res:jd:banded", cookie_pin)


def __is_over_times(biz_id: str, cookie_pin: str, use_times: int) -> bool:
    """是否超过使用上限"""

    key = f"res:jd:use:{biz_id}:{cookie_pin}:*"
    keys_list = rds.client.keys(key)
    length = len(keys_list)
    return length >= use_times


def __add_use_time(biz_id: str, cookie_pin: str, expire: int = 60):
    time_stamp = str(time_lib.current_timestamp10())
    key = f"res:jd:use:{biz_id}:{cookie_pin}:{time_stamp}"
    rds.client.set(key, time_stamp)
    rds.client.expire(key, expire)


def build_res_cookie_object(cookie_str, keys: List[str]) -> ResCookie:
    cookie_obj = json.loads(cookie_str)
    res_obj = ResCookie()
    res_obj.sn = cookie_obj.get("sn")
    res_obj.ua = cookie_obj.get("ua")
    res_obj.uid = cookie_obj.get("uid")

    temp_map = dict()
    cookie_map = cookie_obj.get("cookieMap", {})
    if not keys:
        temp_map = cookie_map
    else:
        for key in keys:
            temp_map[key] = cookie_map.get(key)
    res_obj.cookieMap = temp_map

    return res_obj


def get_cookie(biz_id: str, plat_type: str, keys: List[str], expire: int = 60, use_times: int = 20) -> Optional[ResCookie]:
    """
    根据业务编码获取cookie
    :param biz_id: 业务编号，如：jd-price
    :param plat_type: pc, h5
    :param keys:
    :param expire: 使用过期时间
    :param use_times: 最多使用的次数
    :return:
    """
    rds.client.get('')

    ck_list_key = f"res:jd:{plat_type}:*"
    ck_list = rds.client.keys(ck_list_key)
    cookie_list = get_ck_list(ck_list)
    for cookie_pin in cookie_list:
        if __is_banded(cookie_pin):
            continue
        if __is_over_times(biz_id, cookie_pin, use_times):
            continue
        # 没有禁用 没有达到使用上限
        cookie_key = f"res:jd:{plat_type}:{cookie_pin}"
        cookie_info = rds.client.get(cookie_key)
        res_obj = build_res_cookie_object(cookie_info, keys)
        __add_use_time(biz_id, cookie_pin, expire)
        return res_obj
    return None


def remove_cookie(cookie_pin: str):
    """
    移除cookie
    """
    __banded_cookie(cookie_pin)

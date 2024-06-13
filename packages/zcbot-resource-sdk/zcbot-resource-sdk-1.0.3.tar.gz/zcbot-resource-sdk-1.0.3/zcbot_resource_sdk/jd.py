import json
import random
import logging
from typing import List, Optional, Dict, Any
from zcbot_web_core.lib import time as time_lib
from zcbot_resource_sdk.common.model import ResCookie
from zcbot_resource_sdk.common.redis_client import SingletonRedis

LOGGER = logging.getLogger('京东')
rds = SingletonRedis(redis_uri=None, redis_db=None)


def get_ck_list(origin_key_list: List[str]) -> List[Dict[str, Any]]:
    """
    乱序返回cookie列表， tuple， (sn, pin)
    :param origin_key_list: redis键
    :return: List[Tuple[sn, pin]]
    """
    temp = []

    cookie_values = rds.client.mget(origin_key_list)
    for cookie_str in cookie_values:
        cookie_json = json.loads(cookie_str)
        temp.append(cookie_json)

    random.shuffle(temp)
    return temp


def __is_banded(cookie_pin: str):
    """某个cookie是否被禁用"""
    value = rds.client.get(f"res:jd:banded:{cookie_pin}")
    return value == "1"


def __banded_cookie(cookie_pin: str, freeze_time: int = 7200):
    """禁用某个cookie"""
    key = f"res:jd:banded:{cookie_pin}"
    rds.client.set(key, "1")
    rds.client.expire(key, freeze_time)


def __is_over_times(biz_id: str, cookie_pin: str, use_times: int) -> bool:
    """是否超过使用上限"""

    key = f"res:jd:use:{biz_id}:{cookie_pin}:*"
    keys_list = rds.client.keys(key)
    length = len(keys_list)
    return length >= use_times


def __add_use_time(biz_id: str, cookie_pin: str, expire: int = 60):
    """
    添加一个带有过期时间的key，用以统计短时间内是否达到使用上限
    添加cookie的使用记录，记录时间戳
    :param biz_id:
    :param cookie_pin:
    :param expire: 使用记录的cookie记录
    :return:
    """
    time_stamp = str(time_lib.current_timestamp10())
    key = f"res:jd:use:{biz_id}:{cookie_pin}:{time_stamp}"
    rds.client.set(key, time_stamp)
    rds.client.expire(key, expire)
    record_key = f"res:jd:record:{cookie_pin}"
    rds.client.rpush(record_key, time_stamp)


def build_res_cookie_object(cookie_dict: dict, keys: List[str] = []) -> ResCookie:  # noqa
    res_obj = ResCookie()
    res_obj.sn = cookie_dict.get("sn")
    res_obj.ua = cookie_dict.get("ua")
    res_obj.uid = cookie_dict.get("uid")

    temp_map = dict()
    cookie_map = cookie_dict.get("cookieMap", {})
    if not keys:
        temp_map = cookie_map
    else:
        for key in keys:
            temp_map[key] = cookie_map.get(key)
    res_obj.cookieMap = temp_map

    return res_obj


def get_settings(biz_id: str) -> dict:
    temp = {"expire": 60, "use_times": 20}
    json_str = rds.client.get(f"res:settings:{biz_id}")
    if not json_str:
        return temp
    json_obj = json.loads(json_str)

    temp.update(json_obj)
    return temp


def __is_correct_channel(cookie_info: dict, channel: str = None) -> bool:
    if not channel:
        return True
    cookie_channel = cookie_info.get("channel")
    return cookie_channel == channel


def get_cookie(biz_id: str, keys: List[str] = []) -> Optional[ResCookie]:  # noqa
    """
    根据业务编码获取cookie
    :param biz_id: 业务编号，如：jd-price
    :param keys: 需要提取的cookie字段，如果为空则获取所有
    :return:
    config: plat_type: str, pc, h5
            expire: int, 使用过期时间
            use_times: 最多使用的次数
            channel: 来源
            freeze_time: 禁用时间，京东默认冻结俩小时
    """
    config = get_settings(biz_id)
    expire = config.get("expire")
    use_times = config.get("use_times")
    channel = config.get("channel")
    plat_type = config.get("plat_type", "pc")

    ck_list_key = f"res:jd:{plat_type}:*"
    ck_list = rds.client.keys(ck_list_key)
    cookie_list = get_ck_list(ck_list)
    for cookie_info in cookie_list:
        cookie_pin = cookie_info.get("uid")
        if __is_banded(cookie_pin):
            continue
        if __is_over_times(biz_id, cookie_pin, use_times):
            continue
        # 没有禁用 没有达到使用上限

        # 判断来源是否一致
        correct = __is_correct_channel(cookie_info, channel)
        if not correct:
            continue
        res_obj = build_res_cookie_object(cookie_info, keys)
        __add_use_time(biz_id, cookie_pin, expire)
        return res_obj
    return None


def remove_cookie(biz_id: str, cookie_pin: str):
    """
    移除cookie
    """
    config = get_settings(biz_id)
    freeze_time = config.get('freeze_time', 7200)
    __banded_cookie(cookie_pin, freeze_time)


def release_cookie(cookie_pin: str):
    """
    把移除的cookie释放，解冻
    """
    rds.client.delete(f"res:jd:banded:{cookie_pin}")




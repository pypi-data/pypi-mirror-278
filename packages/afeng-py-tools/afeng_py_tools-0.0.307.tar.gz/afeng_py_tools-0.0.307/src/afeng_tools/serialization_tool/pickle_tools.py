"""
pickle序列化与反序列化工具
"""
import pickle
from typing import Any


def save_list_to_file(obj_list: list[object], save_file: str):
    """保存列表到文件"""
    with open(save_file, "wb") as f:
        # 序列化
        pickle.dump(len(obj_list), f)
        for tmp_obj in obj_list:
            # 序列化
            pickle.dump(tmp_obj, f)


def save_to_file(obj: object, save_file: str):
    """保存到文件"""
    if isinstance(obj, list):
        save_list_to_file(obj, save_file)
    else:
        with open(save_file, "wb") as f:
            # 序列化
            pickle.dump(obj, f)


def parse_to_obj_list(save_file: str) -> list[Any]:
    """保存到文件"""
    with open(save_file, "rb") as f:
        list_size = pickle.load(f)
        # 反序列
        return [pickle.load(f) for tmp in range(list_size)]


def parse_to_obj(save_file: str, is_list: bool = True) -> Any | list[Any]:
    """保存到文件"""
    if is_list:
        return parse_to_obj_list(save_file)
    else:
        with open(save_file, "rb") as f:
            # 反序列
            return pickle.load(f)

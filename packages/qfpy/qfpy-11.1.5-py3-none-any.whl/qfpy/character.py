"""
def to_simplified_chinese(string: str) -> str

def extract_valid_char(string: str) -> str
"""

import re

import zhconv


def to_simplified_chinese(string: str) -> str:
    """
    转为简体中文
    """
    return zhconv.convert(string, "zh-cn")


def extract_valid_char(string: str) -> str:
    """
    提取有效字符

    包括：中文、英文、数字、减号、下划线、点
    """
    return "".join(re.findall("[\u4e00-\u9fa5a-zA-Z0-9\-_.]", string))

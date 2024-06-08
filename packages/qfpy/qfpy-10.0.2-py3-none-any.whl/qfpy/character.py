"""
def to_simplified_chinese(string: str) -> str
"""

import zhconv


def to_simplified_chinese(string: str) -> str:
    """
    转为简体中文
    """
    return zhconv.convert(string, "zh-cn")

"""
def assert_python_version(python_version: str)
"""

import sys


def assert_python_version(python_version: str):
    """
    描述：指定 python 版本，不满足则抛出异常

    参数
    - require_version：str，指定的版本号，如 3.12.3

    返回：
    - 无
    """
    vf = sys.version_info
    current = (vf.major, vf.minor, vf.micro)
    require = tuple(map(int, python_version.split(".")))

    assert current >= require, f"程序要求 Python 版本 >= {python_version}"

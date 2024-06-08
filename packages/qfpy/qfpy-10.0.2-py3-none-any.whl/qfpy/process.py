"""
def exist(process_name: str) -> bool

def not_exit(process_name: str) -> bool
"""

import psutil


def exist(process_name: str) -> bool:
    """
    检查指定的进程是否 存在
    
    参数:
    - process_name: str，要检查的进程名称（不包含扩展名）
    
    返回值:
    - bool，如果进程正在运行，则返回True；否则返回False
    """
    # 检查进程名是否以".exe"结尾，若不结束，则添加".exe"
    if not process_name.endswith(".exe"):
        process_name += ".exe"
    
    # 遍历所有运行的进程，忽略大小写比较进程名
    for p in psutil.process_iter():
        if process_name in p.name().lower():
            return True  # 找到匹配的进程，返回True
    
    return False  # 未找到匹配的进程，返回False

def not_exit(process_name: str) -> bool:
    """
    描述：检查指定的进程是否 不存在
    
    参数
    - process_name：str，要检查的进程名称（不包含扩展名）
    
    返回
    - bool
    """
    return not exist(process_name)


if __name__ == "__main__":
    print(exist("clash verge"))
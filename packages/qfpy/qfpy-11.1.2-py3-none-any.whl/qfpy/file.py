"""
def rename_file(old_path: str | Path, new_name: str) -> Path
"""

from pathlib import Path


def rename_file(old_path: str | Path, new_name: str) -> Path:
    """
    描述：重命名文件

    参数
    - old_path：旧文件路径
    - new_name：新文件名

    返回：新文件路径

    文件名冲突处理：添加后缀 _new
    """
    if not isinstance(old_path, Path):
        old_path = Path(old_path)

    new_path = old_path.parent / new_name

    while True:
        if new_path.exists():
            new_path = old_path.with_stem(old_path.stem + "_new")

        if not new_path.exists():
            old_path.rename(new_path)
            break

    return new_path

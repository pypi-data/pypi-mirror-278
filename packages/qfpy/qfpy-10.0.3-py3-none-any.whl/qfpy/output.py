"""
def remove_color_code(string) -> str
"""
import re


def remove_color_code(string: str) -> str:
   """
   清除颜色代码

   示例

   [1;35mxy,gr,012,lsb,cf                  [0m

   ↓

   xy,gr,012,lsb,cf
   """
   pattern = r'\x1b(\[.*?[@-~]|\].*?(\x07|\x1b\\))'
   return re.sub(pattern, '', string)
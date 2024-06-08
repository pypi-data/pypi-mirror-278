"""
def caesar_encode(text: str, shift=3) -> str

def get_md5_str(s: str) -> str

def rot13(s: str) -> str

def aes_ecb_decrypt(cipher: str, key: str, key_size: int = 16) -> str
"""

import hashlib
import string
from base64 import b64decode

from chepy import Chepy
from Crypto.Cipher import AES


def caesar_encode(text: str, shift=3) -> str:
    """
    凯撒编码

    编码和解码都用这个函数，只需要保证偏移相同

    shift: 偏移量，默认为 3
    """
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(shifted_alphabet, alphabet)
    return text.translate(table)


def get_md5_str(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()


def rot13(s: str) -> str:
    """
    ROT13 编码

    编码和解码都用这个函数
    """
    return Chepy(s).rot_13().out.decode()


def _zero_padding(string: str, length: int) -> str:
    """
    用 0 填充
    """
    b = string.encode()
    b += b"\x00" * (length - len(b))
    return b

def aes_ecb_decrypt(cipher: str, key: str, key_size: int = 16) -> str:
    """
    aes ecb 模式解密

    key_size: 密钥长度，默认为 16，单位是字节，还可以是 24、32
    """
    cipher = b64decode(cipher)
    key = _zero_padding(key, key_size)
    return AES.new(key, AES.MODE_ECB).decrypt(cipher).decode()
    

if __name__ == "__main__":
    print(aes_ecb_decrypt("7SsQWmZ524i/yVWoMeAIJA==", "weigongcun"))
#!/usr/bin/env python3
# coding:utf-8


import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from functools import wraps
from myutils.logger import Logger

__author__ = 'rootklt'
__license__ = '1.0.0'

logger = Logger('aes')


def exceptions(func):
    '''
    异常处理装饰器
    '''
    @wraps(func)
    def do_except(*args, **kwargs):
        ret = b''
        try:
            ret = func(*args, **kwargs)
        except UnicodeDecodeError as e:
            logger.error('失败,请检查密钥是否正确!')
            logger.exception(e)
        except binascii.Error as e:
            logger.exception(e)
        except Exception as e:
            logger.exception(e)
        finally:
            return ret
    return do_except


class AESCrypt:
    '''
    AES加解密,支持ECB 和 CBC模式
    '''

    def __init__(self, key, iv=None, pad_mode='pkcs7'):
        '''
        使用密钥,加密模式进行初始化
        :param key str or bytes: 加密密钥
        :param iv str or bytes: 初始向量
        :param pad_mode str: 填充方式 zero 或pkcs7, default pkcs7
        '''

        self.init(key, iv)
        self.block_size = AES.block_size
        self.pad_mode = pad_mode

    def init(self, key, iv):
        self.key = key if isinstance(key, bytes) else key.encode()
        if len(self.key) != AES.block_size:
            raise RuntimeError(f'密钥长度非{AES.block_size}位!!!')
        self.iv = iv or bytes(AES.block_size)
        self.iv = self.iv if isinstance(self.iv, bytes) else self.iv.encode()

    def check_input(self, input_data):
        return input_data if isinstance(input_data, bytes) else input_data.encode()

    def _pad(self, text):
        text = self.check_input(text)
        pad_len = len(text) % self.block_size
        if self.pad_mode == 'zero':
            return text + b'\0'*(self.block_size - pad_len)
        return pad(text, block_size=self.block_size, style='pkcs7')

    def _unpad(self, text):
        text = self.check_input(text)
        if self.pad_mode == 'zero':
            return text.strip(b'\0')
        return text[:-text[-1]]

    @exceptions
    def encrypt_ecb(self, plaintext) -> bytes:
        """
        AES ECB模式加密
        :param plaintext: 明文
        :return ciphertext: 密文
        """

        cryptor = AES.new(self.key, AES.MODE_ECB)
        return cryptor.encrypt(self._pad(plaintext))

    @exceptions
    def decrypt_ecb(self, ciphertext) -> bytes:
        """
        AES ECB模式解密
        :param ciphertext: 密文
        :return plaintext: 明文
        """
        ciphertext = self.check_input(ciphertext)  # 转成bytes
        cryptor = AES.new(self.key, AES.MODE_ECB)
        decrypt_text = cryptor.decrypt(ciphertext)
        return self._unpad(decrypt_text)

    @exceptions
    def encrypt_cbc(self, plaintext) -> bytes:
        """
        AES CBC模式加密
        :param plaintext: 明文
        :return ciphertext: 密文
        """

        cryptor = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cryptor.encrypt(self._pad(plaintext))

    @exceptions
    def decrypt_cbc(self, ciphertext) -> bytes:
        """
        AES CBC模式解密
        :param ciphertext: 密文
        :return plaintext: 明文
        """

        ciphertext = self.check_input(ciphertext)  # 转成bytes
        cryptor = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypt_text = cryptor.decrypt(ciphertext)
        return self._unpad(decrypt_text)

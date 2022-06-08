#!/usr/bin/env python3
#coding:utf-8

from myutils import session,AESCrypt,timestamp_str
from myutils.timeUtils import get_date

url = 'http://www.sina.cn'
session.get(url)
print(session.get_content())

key = '12345678'*2
aes = AESCrypt(key, iv = '0000000012345678')
enc = aes.encrypt_cbc('hello')
dec = aes.decrypt_cbc(enc)
assert dec == b'hello'

t = timestamp_str('ms')
print(t)
print(get_date())
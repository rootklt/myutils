# 自己整理的一些常用工具集

## 目录结构

```bash
├── README.md
├── myutils
│   ├── __init__.py
│   ├── aesUtils.py
│   ├── httpUtils.py
│   ├── loggerUtils.py
│   └── timeUtils.py
├── requirements.txt
├── setup.py
└── tests
    ├── clogger_test.py
    └── util_test.py
```

## HTTP请求工具

### 工具目标

最近写代码遇到各种http请求，在脚本中用requests库写的请求，再次使用得根据请求方法来修改，每个请求还需要配上一大段异常处理。这些代码结构上都相差无几，直接封装可以提高效率。
使用一个异常处理装饰器，可对不同请求方法进行封装，减少代码量。

```python
#logger也是使用了loggerUtils中对logging的封装，在控制台和日志文件中记录信息，控制台以不同颜色区分日志级别。
logger = Logger('httpUtils')
def exceptions(func):
    '''
    异常处理装饰器
    '''
    @wraps(func)
    def do_except(*args, **kwargs):
        response = requests.Response()
        try:
            response = func(*args, **kwargs)
        except TimeoutError:
            logger.warning('[-]请求超时')
        except Exception as e:
            logger.error(f'[-]出错=>{e}')
        finally:
            return response
    return do_except

#在类方法中进行装饰，如下。
    @classmethod
    @exceptions
    def post(cls, *args, **kwargs) -> requests.Response:
        '''
        POST请求，参数与requests中参数一致
        '''
        cls.response = cls.session.post(*args, **kwargs)
        return cls.response
```

封装的http请求方法中，可以直接返回response类型。同时也可以通过以下方法来获取相应的响应内容，如json->dict, xml->dict, 如果response中没有json或xml，将返回None：

```python
    @classmethod
    @exceptions
    def get_json(cls) -> dict:
        '''
        响应为json格式时，获取dict类型的内容
        '''
        return cls.response.json()

    @classmethod
    @exceptions
    def get_xml(cls) -> dict:
        '''
        响应为xml格式时，将xm转换成dict类型的内容
        '''
        return xmltodict.parse(cls.response.content)
```

### 使用方法

```python
from myutils import session
url = 'http://www.baidu.com'
resp = session.get(url)


assert resp.content == session.get_content()
assert session.get_json() == None   #因为返回的是html，不是json，所以get_json()解析异常，返回None
```

## AES加解密

### 工具目标

因为有需求，所以才会去做封装以方便工具，在编写poc或exp时会用到aes来加解密，频度比较高的是AES的ECB和CBC两种模式，所以将这两种模式进行封装。

```python
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
```

### 使用方法

```python

from myutils import AESCrypt

key = '1234567812345678'
iv = bytes(16)
plaintext = 'helloworld'

#ECB时不需要设置iv
aes = AESCrypt(key)
cipher = aes.encrypt_ecb(plaintext)
dec_plain = aes.decrypt_ecb(cipher)
assert dec_plain.decode() == plaintext

#CBC加解密
aes = AESCrypt(key, iv)
cipher = aes.encrypt_cbc(plaintext)
dec_plain = aes.decrypt_cbc(cipher)
assert dec_plain.decode() == plaintext

#填充模式默认是pkcs7，支持zero填充
```

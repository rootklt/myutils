#!/usr/bin/env python3
#coding:utf-8

import logging
import traceback
import requests
import xmltodict
from requests.adapters import HTTPAdapter,Retry
from functools import wraps


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
            logging.warning('[-]请求超时')
        except Exception as e:
            traceback(e)
            logging.warning(f'[-]出错=>{e}')
        finally:
            return response
    return do_except


class HTTPRequest(object):
    session = requests.Session()
    response = requests.Response()
    def __init__(self):
        pass
        #self.set_read_count(1)

    def set_read_count(self, count):
        '''
        设置重读次数，避免在多线程或多进程中由于"Connection: close"而造成读超时，需要在请求发起之前设置
        :param: count: int 重读次数
        '''
        self.session.mount('http://', HTTPAdapter(max_retries = Retry(read = count, allowed_methods = ['POST', 'GET'])))
        self.session.mount('https://', HTTPAdapter(max_retries = Retry(read = count, allowed_methods = ['POST', 'GET'])))
    
    @classmethod
    @exceptions
    def post(cls, *args, **kwargs) ->requests.Response:
        '''
        POST请求，参数与requests中参数一致
        '''
        cls.response = cls.session.post(*args, **kwargs)
        return cls.response

    @classmethod
    @exceptions
    def get(cls, *args, **kwargs) -> requests.Response:
        '''
        GET请求，参数与requests中参数一致
        '''
        cls.response = cls.session.get(*args, **kwargs)
        return cls.response

    @staticmethod
    @exceptions
    def delete(cls, *args, **kwargs) -> requests.Response:
        '''
        DELETE请求，参数与requests中参数一致
        '''
        cls.response = cls.session.delete(*args, **kwargs)
        return cls.response

    @staticmethod
    @exceptions
    def put(cls, *args, **kwargs) -> requests.Response:
        '''
        PUT请求，参数与requests中参数一致
        '''
        return cls.session.put(*args, **kwargs)

    @classmethod
    @exceptions
    def head(cls, *args, **kwargs) -> requests.Response:
        '''
        HEAD请求，参数与requests中参数一致
        '''
        cls.response = cls.session.head(*args, **kwargs)
        return cls.response

    @classmethod
    @exceptions
    def get_json(cls) ->dict:
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
    
    @classmethod
    @exceptions
    def get_content(cls) -> bytes:
        return cls.response.content
    
    @classmethod
    @exceptions
    def get_text(cls) -> str:
        return cls.response.text

    @classmethod
    @exceptions
    def get_header(cls) -> dict:
        return cls.response.headers
    
    @classmethod
    @exceptions
    def get_code(cls):
        return cls.response.status_code

session = HTTPRequest()
if __name__ == '__main__':
    
    url = 'http://www.baidu.com'
    resp = session.get(url)
    header = session.get_header()
    print(header)
    
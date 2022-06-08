#!/usr/bin/env python3
#coding:utf-8

import time
import datetime


def timestamp(ms = ''):
    '''
    生成秒或毫秒时间戳
    :param: ms str: 当设置ms = 'ms'时，则生成毫秒（13位）时间戳，否则是秒级的
    :return: int: 返回整形时间戳
    '''
    return int(round(time.time()*1000)) if ms == 'ms' else int(time.time())

def timestamp_str(ms = ''):
    '''
    生成秒或毫秒时间戳
    :param: ms str: 当设置ms = 'ms'时，则生成毫秒（13位）时间戳，否则是秒级的
    :return: str: 返回字符类型的时间戳
    '''
    return str(timestamp(ms))

def datetime_to_timestamp(time_str: str = ''):
    fmt = '%Y-%m-%d %H:%M:%S'
    if not time_str:
        time_str = time.strftime(fmt, time.localtime())
    t = datetime.datetime.strptime(time_str, fmt)
    stamp = time.mktime(t.timetuple())
    return int(stamp)

def timestamp_to_datetime(time_int:float = 0.0):
    if time_int == 0.0:
        time_int = time.time()
    elif len(str(time_int)) == 13:
        time_int = time_int/1000
        
    d = datetime.datetime.fromtimestamp(time_int)

    return d.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
def get_time():
    return datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S')

def get_date():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

if __name__ == '__main__':
    print(get_time())
    print(get_date())
    print(timestamp_to_datetime(1654702839100))
    print(datetime_to_timestamp())
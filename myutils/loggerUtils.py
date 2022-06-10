#!/usr/bin/env python3
# coding:utf-8


import logging
import colorama
from myutils.timeUtils import get_date


# 设置自动重置
colorama.init(autoreset=True)
Fore = colorama.Fore

# 配置默认文件和日志格式
LOG_FILE = f'./logger-{get_date()}.log'
FORMATTER = logging.Formatter(
    fmt="%(asctime)s %(levelname)s [%(name)s] [%(filename)s (%(funcName)s:%(lineno)d)] - %(message)s", datefmt="%Y-%m-%d %X")


class Logger():
    '''
    在终端显示不同颜色
    '''

    def __init__(self, name, fmt=FORMATTER, log_file=LOG_FILE, level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.file_handler = logging.FileHandler(log_file, encoding='utf-8')
        self.console_handler = logging.StreamHandler()
        self.formatter = fmt
        self.file_handler.setFormatter(fmt)
        self.logger.setLevel(level)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)

    def set_formatter(self, fmt, datefmt='%Y-%m-%d %X',  * args, **kwargs):
        self.formatter = logging.Formatter(
            fmt=fmt, datefmt=datefmt, *args, **kwargs)
        self.file_handler.setFormatter(self.formatter)

    def set_console_color(self, color):
        fmt = color + self.formatter._fmt
        self.console_handler.setFormatter(
            logging.Formatter(fmt=fmt))

    def fatal(self, msg, *args, **kwargs):
        self.set_console_color(Fore.LIGHTRED_EX)
        return self.logger.fatal(f'{msg}', *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.set_console_color(Fore.LIGHTRED_EX)
        return self.logger.critical(f'{msg}', *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.set_console_color(Fore.RED)
        return self.logger.error(f'{msg}', *args, **kwargs)

    def exceptioin(self, msg, *args, **kwargs):
        self.set_console_color(Fore.RED)
        return self.logger.exception(f'{msg}', *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.set_console_color(Fore.LIGHTYELLOW_EX)
        return self.logger.warning(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.set_console_color(Fore.CYAN)
        return self.logger.debug(f'{msg}', *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.set_console_color(Fore.WHITE)
        return self.logger.info(f'{msg}', *args, **kwargs)

    def success(self, msg, *args, **kwargs):
        self.set_console_color(Fore.GREEN)
        return self.logger.info(f'{msg}', *args, **kwargs)

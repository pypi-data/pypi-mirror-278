#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/6/12 下午7:34
@Author  : Gie
@File    : iaarLogger.py
@Desc    :
"""
import logging
import os
import sys
from datetime import datetime


def log_date_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%S")


def formatted_iaar_log_msg(msg, level, class_name='', line_num='', track_id=''):
    formatted_level = '{0:>8}'.format(f'{level}')
    return f'[{log_date_time()}  {formatted_level}] {class_name}:{line_num} {msg} {track_id}'


class iaarLogger:
    def __init__(self, script_name, default_level="DEBUG"):
        self._msg = ''
        self._level = ''
        self._track_id = ''
        self._line_num = ''
        self._name = script_name
        self._log = logging.getLogger(script_name)
        self._handler = logging.StreamHandler(sys.stdout)
        self._log.setLevel(default_level)
        self._log.addHandler(self._handler)

    def debug(self, msg):
        self._msg = msg
        self._level = 'DEBUG'
        # self._log.setLevel(10)
        return self

    def info(self, msg):
        self._msg = msg
        self._level = 'INFO'
        # self._log.setLevel(20)
        return self

    def warning(self, msg):
        self._msg = msg
        self._level = 'WARNING'
        # self._log.setLevel(30)
        return self

    def error(self, msg):
        self._msg = msg
        self._level = 'ERROR'
        # self._log.setLevel(40)
        return self

    def critical(self, msg):
        self._msg = msg
        self._level = 'CRITICAL'
        # self._log.setLevel(50)
        return self

    def track_id(self, track_id=''):
        self._track_id = track_id
        formatted_msg = formatted_iaar_log_msg(
            self._msg,
            self._level,
            class_name=self._name,
            line_num=self._line_num,
            track_id=self._track_id)

        formatter = logging.Formatter(formatted_msg)
        self._handler.setFormatter(formatter)
        self._log.info(formatted_msg)
        return self

    def commit(self):
        pass


if __name__ == '__main__':
    logger = iaarLogger(os.path.basename(sys.argv[0]))
    logger.info('info 级别日志测试 info').track_id('test_track_id_info').commit()
    logger.debug('debug 级别日志测试 debug').track_id('test_track_id_debug').commit()
    logger.error('error 级别日志测试 debug').track_id('test_track_id_error').commit()
    logger.warning('warning 级别日志测试 debug').track_id('test_track_id_warning').commit()

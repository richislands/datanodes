#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
import logging.handlers
import logging
import os
import sys

class logger2:
    def __init__(self, logger, log_path, log_size=8, log_number=10):
        # 创建一个logger
        self.logger = logging.getLogger()

        # 日志格式，可以根据需要设置
        fmt = logging.Formatter('[%(asctime)s][%(filename)s][line:%(lineno)d]\
            [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')

        # 日志文件名
        logname = os.path.join(log_path,'log.txt')
        print(logname)

        # 日志输出到文件，这里用到了上面获取的日志名称，大小，保存个数
        handle_file = logging.handlers.RotatingFileHandler(logname, maxBytes=log_size, backupCount=log_number)
        handle_file.setFormatter(fmt)
        handle_file.setLevel(logging.INFO)

        # 同时输出到屏幕
        handle_console = logging.StreamHandler(stream=sys.stdout)
        handle_console.setFormatter(fmt)
        handle_console.setLevel(logging.DEBUG)

        self.logger.addHandler(handle_file)
        self.logger.addHandler(handle_console)

    def getlog(self):
        return self.logger





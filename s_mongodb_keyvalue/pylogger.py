#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'cuiwei'
__version__ = '0.1.0.0'

import os
import time
import logging.handlers
import platform

# Global logger
g_logger = None

if platform.system() == 'Windows':
    from ctypes import windll, c_ulong
    
    def color_text_decorator(function):
        def real_func(self, string):
            windll.Kernel32.GetStdHandle.restype = c_ulong
            h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))
            if function.__name__.upper() == 'ERROR':
                windll.Kernel32.SetConsoleTextAttribute(h, 12)
            elif function.__name__.upper() == 'WARN':
                windll.Kernel32.SetConsoleTextAttribute(h, 13)
            elif function.__name__.upper() == 'INFO':
                windll.Kernel32.SetConsoleTextAttribute(h, 14)
            elif function.__name__.upper() == 'DEBUG':
                windll.Kernel32.SetConsoleTextAttribute(h, 15)
            else:
                windll.Kernel32.SetConsoleTextAttribute(h, 15)
            function(self, string)
            windll.Kernel32.SetConsoleTextAttribute(h, 15)
        return real_func
else:
    def color_text_decorator(function):
        def real_func(self, string):
            if function.__name__.upper() == 'ERROR':
                self.stream.write('\033[0;31;40m')
            elif function.__name__.upper() == 'WARN':
                self.stream.write('\033[0;35;40m')
            elif function.__name__.upper() == 'INFO':
                self.stream.write('\033[0;33;40m')
            elif function.__name__.upper() == 'DEBUG':
                self.stream.write('\033[0;37;40m')
            else:
                self.stream.write('\033[0;37;40m')
            function(self, string)
            self.stream.write('\033[0m')
        return real_func

FORMAT = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'

class Logger(object):
    LOG_LEVEL = 5
    def __init__(self, name, path=None, logname=None, maxBytes=10 * 1024 * 1024, backupCount=10):
        self.name = name
        self.path = path if path is not None else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        if not os.path.exists(self.path):
            os.makedirs(path)
        # baseconfig
        logging.basicConfig()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(FORMAT)

        # output to terminal
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(logging.DEBUG)
        self.logger.addHandler(sh)
        self.stream = sh.stream

        # output to file
        logname = logname if logname is not None else 's_mongodb_keyvalue.txt'
        file_rf = logging.handlers.RotatingFileHandler(os.path.join(path, logname), \
            mode='a', maxBytes=maxBytes, backupCount=backupCount, encoding='utf-8')
        file_rf.setFormatter(formatter)
        file_rf.setLevel(logging.DEBUG)
        self.logger.addHandler(file_rf)

        # 防止在终端重复打印
        self.logger.propagate = 0

    @color_text_decorator
    def hint(self, string):
        strTmp = str(string)
        strTmp = ' '.join(strTmp.split())
        if self.LOG_LEVEL >= 5:
            return self.logger.debug(strTmp)

    @color_text_decorator
    def debug(self, string):
        strTmp = str(string)
        strTmp = ' '.join(strTmp.split())
        if self.LOG_LEVEL >= 4:
            return self.logger.debug(strTmp)

    @color_text_decorator
    def info(self, string):
        strTmp = str(string)
        strTmp = ' '.join(strTmp.split())
        if self.LOG_LEVEL >= 3:
            return self.logger.info(strTmp)

    @color_text_decorator
    def warn(self, string):
        strTmp = str(string)
        strTmp = ' '.join(strTmp.split())
        if self.LOG_LEVEL >= 2:
            return self.logger.warn(strTmp)

    @color_text_decorator
    def error(self, string):
        strTmp = str(string)
        strTmp = ' '.join(strTmp.split())
        if self.LOG_LEVEL >= 1:
            return self.logger.error(strTmp)

class TestLogModule(object):
    def runtest(self):
        # logger = Logger('TEST',logname='log_test.txt',\
        # path= os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mylog'),\
        # size = 100*100, number=10)
        logger = Logger('TEST', maxBytes=100 * 100, backupCount=10)
        logger.LOG_LEVEL = 5

        iCount = 0
        while True:
            iCount = iCount + 1
            logger.error(str(iCount))
            logger.debug('debug test...........')
            logger.info('info  test.............')
            logger.warn('warn  test.............')
            logger.error('error test...........')
            time.sleep(1)
            if iCount >= 1200:
                break

# if __name__ == '__main__':
#     TestLogModule().runtest()







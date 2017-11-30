#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import logging
import logging.handlers
import platform

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

class MainLogger(object):
    DEBUG_MODE = True
    LOG_LEVEL = 5

    def __init__(self, name, path=None):
        current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log_test')
        if not os.path.exists(current_path):
            os.makedirs(current_path)

        # baseconfig
        logging.basicConfig()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(FORMAT)

        th_all = logging.handlers.TimedRotatingFileHandler(os.path.join(current_path, \
            'trfh.log'), when='M', interval=5, backupCount=7)
        th_all.setFormatter(formatter)
        th_all.setLevel(logging.DEBUG)
        self.logger.addHandler(th_all)

        rh_all = logging.handlers.RotatingFileHandler(os.path.join(current_path, \
            'rfh.log'), mode='a', maxBytes= 1000 * 1000, backupCount=5)
        rh_all.setFormatter(formatter)
        rh_all.setLevel(logging.DEBUG)
        self.logger.addHandler(rh_all)

        # 防止在终端重复打印
        self.logger.propagate = 0

    def hint(self, string):
        # 去除多余连续空格
        strTmp = str(string)
        strTmp = ' '.join(strTmp.split())
        if self.LOG_LEVEL >= 5:
            return self.logger.debug(strTmp)

    def debug(self, string):
        strTmp = str(string)
        strTmp = ' '.join(strTmp.split())
        if self.LOG_LEVEL >= 4:
            return self.logger.debug(strTmp)

    def info(self, string):
        strTmp = str(string)
        strTmp = ' '.join(strTmp.split())
        if self.LOG_LEVEL >= 3:
            return self.logger.info(strTmp)

    def warn(self, string):
        strTmp = str(string)
        strTmp = ' '.join(strTmp.split())
        if self.LOG_LEVEL >= 2:
            return self.logger.warn(strTmp)

    def error(self, string):
        strTmp = str(string)
        strTmp = ' '.join(strTmp.split())
        if self.LOG_LEVEL >= 1:
            return self.logger.error(strTmp)

main_logger = MainLogger('MasterMainLogger')

class Logger(object):
    DEBUG_MODE = True
    LOG_LEVEL = 5

    def __init__(self, name, filename=None):
        self.name = name
        # baseconfig
        logging.basicConfig()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(FORMAT)

        # output to terminal
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(logging.DEBUG if self.DEBUG_MODE else logging.INFO)
        self.logger.addHandler(sh)
        self.stream = sh.stream

        # output to user define file
        if filename is not None:
            fh = logging.FileHandler(filename, 'a')
            fh.setFormatter(formatter)
            fh.setLevel(logging.DEBUG)
            self.logger.addHandler(fh)
            self.logger.propagate = 0

        # 防止在终端重复打印
        self.logger.propagate = 0

    @color_text_decorator
    def hint(self, string):
        strTmp = str(string)
        strTmp = ' '.join(strTmp.split())
        main_logger.hint("[" + self.name + "] "  + strTmp)
        if self.LOG_LEVEL >= 5:
            return self.logger.debug(strTmp)

    @color_text_decorator
    def debug(self, string):
        strTmp = str(string)
        strTmp = ' '.join(strTmp.split())
        main_logger.debug("[" + self.name + "] "  + strTmp)
        if self.LOG_LEVEL >= 4:
            return self.logger.debug(strTmp)

    @color_text_decorator
    def info(self, string):
        strTmp = str(string)
        strTmp = ' '.join(strTmp.split())
        main_logger.info("[" + self.name + "] "  + strTmp)
        if self.LOG_LEVEL >= 3:
            return self.logger.info(strTmp)

    @color_text_decorator
    def warn(self, string):
        strTmp = str(string)
        strTmp = ' '.join(strTmp.split())
        main_logger.warn("[" + self.name + "] "  + strTmp)
        if self.LOG_LEVEL >= 2:
            return self.logger.warn(strTmp)

    @color_text_decorator
    def error(self, string):
        strTmp = str(string)
        strTmp = ' '.join(strTmp.split())
        main_logger.error("[" + self.name + "] "  + strTmp)
        if self.LOG_LEVEL >= 1:
            return self.logger.error(strTmp)

class TestLogModule(object):
    def runtest(self):
        logger = Logger('TEST')

        iCount = 0
        while True:
            iCount = iCount + 1
            logger.error(str(iCount))
            logger.debug('debug test...........')
            logger.info('info  test.............')
            logger.warn('warn  test.............')
            logger.error('error test...........')
            time.sleep(1)
            if iCount >= 120:
                break

if __name__ == '__main__':
    TestLogModule().runtest()







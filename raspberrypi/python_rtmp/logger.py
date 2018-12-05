#! /usr/bin/python
# -*- coding: utf-8 -*-
import logging
import traceback
from logging.handlers import RotatingFileHandler

class Logger:
    # 单例模式
    @classmethod
    def get_logger(cls):
        if cls.instance:
            return cls.instance
        else:
            obj = cls()
            cls.instance = obj
            return obj

    def __init__(self):
        self.logger = self.__logger_init()

    def __logger_init(self):
        # 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
        log_file = 'capture_video.log'
        Rthandler = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
        Rthandler.setLevel(logging.ERROR)
        formatter = logging.Formatter(
            '\n%(asctime)s   %(filename)s[line:%(lineno)d]   %(levelname)s\n%(message)s')
        Rthandler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.addHandler(Rthandler)
        logger.setLevel(logging.ERROR)
        return logger

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)
        self.logger.error(traceback.format_exc())

    def debug(self, msg):
        self.logger.debug(msg)

    def critical(self, msg):
        self.logger.critical(msg)
        self.logger.critical(traceback.format_exc())
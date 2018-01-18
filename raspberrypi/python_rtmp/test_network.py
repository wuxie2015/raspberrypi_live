# -- coding: utf-8 --
from setting import HOST
import subprocess
import signal
import logging
from logging.handlers import RotatingFileHandler
import os
import time
import sys

# detact whether the video is alive

def logger_init():
    # 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
    log_file = 'test_network.log'
    Rthandler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
    Rthandler.setLevel(logging.INFO)
    formatter = logging.Formatter('\n%(asctime)s   %(filename)s[line:%(lineno)d]   %(levelname)s\n%(message)s')
    Rthandler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(Rthandler)
    logger.setLevel(logging.INFO)
    return logger

def time_limit(interval):
    logger = logger_init()
    def wraps(func):
        def handler(*args, **kwargs):
            logger.error("function %s ruuning out of time" % func.__name__)
            raise RuntimeError()

        def deco(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(interval)
            res = func(*args, **kwargs)
            signal.alarm(0)
            return res
        return deco
    return wraps

def test_net(timeout=30):
    logger = logger_init()
    p = subprocess.Popen(['tcpdump','tcp','port','1935','and','src','host',HOST,' -i','wlan0','-c','10']
                     ,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t_beginning = time.time()
    seconds_passed = 0
    while True:
        seconds_passed = time.time() - t_beginning
        if p.poll() is not None:
            logger.info('check passed')
            break
        if timeout and seconds_passed > timeout:
            p.terminate()
            raise RuntimeError()
        time.sleep(0.1)
    return p.stdout.read()


def main():
    logger = logger_init()
    try:
        test_net()
        sys.exit(0)
    except RuntimeError:
        logger.error('restarting')
        sys.exit(1)

if __name__ == '__main__':
    main()

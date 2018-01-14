# -- coding: utf-8 --
from setting import HOST
import subprocess
import signal
import logging
from logging.handlers import RotatingFileHandler
import os

# detact whether the video is alive

def logger_init():
    # 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
    log_file = 'test_network.log'
    Rthandler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
    Rthandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('\n%(asctime)s   %(filename)s[line:%(lineno)d]   %(levelname)s\n%(message)s')
    Rthandler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(Rthandler)
    logger.setLevel(logging.DEBUG)
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

@time_limit(30)
def test_net():
    os.system('tcpdump tcp port 1935 and host %s  -i wlan0 -c 10' % HOST)


def main():
    try:
        test_net()
    except RuntimeError:
        subprocess.Popen(
            ['sh', '/usr/local/project/raspberrypi_video/raspberrypi/python_rtmp/raspberrypi_video.sh', 'restart'],
            stdout=subprocess.PIPE)

if __name__ == '__main__':
    main()
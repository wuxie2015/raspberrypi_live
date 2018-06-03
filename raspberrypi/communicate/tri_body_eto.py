# -*- coding:utf-8 -*-
from tri_body_yewenjie import ChatClient
import os
import logging
from logging.handlers import RotatingFileHandler
from setting import PASSWORD
import time
import subprocess


def logger_init():
    # 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
    log_file = 'tri_body_eto.log'
    Rthandler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
    Rthandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('\n%(asctime)s   %(filename)s[line:%(lineno)d]   %(levelname)s\n%(message)s')
    Rthandler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(Rthandler)
    logger.setLevel(logging.DEBUG)
    return logger

def get_process_count(process_name):
    cmd1=["ps","-aux"]
    cmd2=["grep",process_name]
    cmd3=["grep","-v","grep"]
    cmd4=["wc","-l"]
    p1 = subprocess.Popen(cmd1,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p2 = subprocess.Popen(cmd2, stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p3 = subprocess.Popen(cmd3, stdin=p2.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p4 = subprocess.Popen(cmd4, stdin=p3.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process_count_str = p4.stdout.read().decode('utf8')
    process_count = int(process_count_str)
    return process_count


def call_back_fun(self,data):
    logger = logger_init()
    logger.info("recieved data %s"%data)
    try:
        remote_id = data.split('||')[0]
        command = data.split('||')[1]
    except IndexError:
        logger.info('not a command')
    else:
        logger.info(command)
        logger.info(type(command))
        if str(remote_id) == '1':
            if command == '0':
                logger.info("recieved command reboot from %s" % (remote_id))
                time.sleep(1)
                self.send_once("recieved command reboot",remote_id)
                os.system('reboot')
            elif command == '1':
                logger.info("recieved command start camera from %s" % (remote_id))
                os.system('sh /usr/local/project/raspberrypi_video/raspberrypi/python_rtmp/raspberrypi_video.sh watchdog')
                time.sleep(1)
                self.send_once("recieved command start camera", remote_id)
            elif command == '2':
                logger.info("recieved command 'restart camera from %s" % (remote_id))
                os.system('sh /usr/local/project/raspberrypi_video/raspberrypi/python_rtmp/raspberrypi_video.sh stop')
                os.system('sh /usr/local/project/raspberrypi_video/raspberrypi/python_rtmp/raspberrypi_video.sh watchdog')
                time.sleep(1)
                self.send_once("recieved command restart camera", remote_id)
            elif command == '3':
                logger.info("recieved command close camera from %s" % (remote_id))
                os.system('sh /usr/local/project/raspberrypi_video/raspberrypi/python_rtmp/raspberrypi_video.sh stop')
                time.sleep(1)
                self.send_once("recieved command close camera", remote_id)
            elif command == '4':
                logger.info("recieved command check camera status %s" % (remote_id))
                process_count = get_process_count('capture_video.py')
                time.sleep(1)
                self.send_once("recieved command check camera, process count is %s"%process_count, remote_id)
            elif command == '100':
                logger.info("recieved command test from %s" % (remote_id))
                time.sleep(1)
                self.send_once("recieved command test", remote_id)
            else:
                logger.info('invalid data')
        else:
            logger.error('wrong remote from %s'%remote_id)


def main_loop():
    logger = logger_init()
    while True:
        try:
            chat_obj = ChatClient('0', PASSWORD)
            chat_obj.connect_program()
            try:
                chat_obj.socket_handler_program(call_back_fun)
            except RuntimeError:
                pass
            chat_obj.close()
            logger.info('reconnecting')
        except Exception as e:
            logger.critical("Crittical Error occured %s"%e)

if __name__ == '__main__':
    main_loop()

# -*- coding:utf-8 -*-
from tri_body_yewenjie import ChatClient
import os
import logging
from logging.handlers import RotatingFileHandler
from setting import PASSWORD
import json



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

def call_back_fun(data):
    logger = logger_init()
    logger.info("recieved data %s"%data)
    try:
        data_dict = json.loads(data)
    except BaseException as e:
        data_dict = {}
        logger.error(e.args)
        return None
    else:
        temperature = data_dict['temperature']
        return temperature

    # try:
    #     remote_id = data.split('||')[0]
    #     command = data.split('||')[1]
    # except IndexError:
    #     logger.info('not a command')
    # else:
    #     print(command)
    #     print(type(command))
    #     print(type('1'))
    #     if str(remote_id) == '1':
    #         if command == '0':
    #             logger.info("recieved command reboot from %s" % (remote_id))
    #             os.system('reboot')
    #         elif command == '1':
    #             logger.info("recieved command start camera from %s" % (remote_id))
    #             os.system('sh /usr/local/project/raspberrypi_video/raspberrypi/python_rtmp/raspberrypi_video.sh start')
    #         elif command == '2':
    #             logger.info("recieved command 'restart camera from %s" % (remote_id))
    #             os.system('sh /usr/local/project/raspberrypi_video/raspberrypi/python_rtmp/raspberrypi_video.sh stop')
    #             os.system('sh /usr/local/project/raspberrypi_video/raspberrypi/python_rtmp/raspberrypi_video.sh start')
    #         elif command == '3':
    #             logger.info("recieved command close camera from %s" % (remote_id))
    #             os.system('sh /usr/local/project/raspberrypi_video/raspberrypi/python_rtmp/raspberrypi_video.sh stop')
    #         else:
    #             logger.info('invalid data')
    #     else:
    #         logger.error('wrong remote from %s'%remote_id)


def main_loop():
    chat_obj = ChatClient('1', PASSWORD)
    chat_obj.connect_program()
    chat_obj.socket_handler_program(call_back_fun)
    chat_obj.close()


if __name__ == '__main__':
    main_loop()

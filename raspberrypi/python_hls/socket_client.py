#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import socket
import struct
from optparse import OptionParser
from setting import HOST,PORT
import hashlib
from rabbitmq_util import consumer
import logging
from logging.handlers import RotatingFileHandler


def logger_init():
    # 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
    log_file = 'socket_client.log'
    Rthandler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
    Rthandler.setLevel(logging.INFO)
    formatter = logging.Formatter('\n%(asctime)s   %(filename)s[line:%(lineno)d]   %(levelname)s\n%(message)s')
    Rthandler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(Rthandler)
    logger.setLevel(logging.INFO)
    return logger

logger = logger_init()

def connect():
    remote_ip = HOST
    port = PORT
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(2)
    try:
        client_socket.connect((remote_ip, port))
    except Exception as e:
        logger.error('Unable to connect because of %s' % e)
        return None
    else:
        logger.info('Connected to remote host. Start sending messages')
        return client_socket


def close(client_socket):
    try:
        client_socket.close()
    except Exception as e:
        logger.error('Unable to deconnect because of %s' % e)
        return False
    else:
        logger.info('DeConnected to remote host. Start sending messages')
        return True

def calc_md5(f_name):
    with open(f_name, 'rb') as fr:
        md5 = hashlib.md5()
        md5.update(fr.read())
        md5 = md5.hexdigest()
    return md5

def sendf(ch, method, properties, body):
    file_path = body
    try:
        client_socket = connect()
        if client_socket is not None:
            if os.path.isfile(file_path):
                fileinfo_size = struct.calcsize('128sI')  # 定义打包规则
                # 定义文件头信息，包含文件名和文件大小
                md5 = calc_md5(file_path)
                md5 = md5.encode('utf8')
                f_name_bytes = os.path.basename(file_path).encode('utf8')
                f_name_length = len(f_name_bytes)
                fhead = struct.pack('128sII32s', f_name_bytes, f_name_length, os.stat(file_path).st_size, md5)
                logger.info('start send file %s length %s md5 %s' % (file_path, os.stat(file_path).st_size, md5))
                # fhead = struct.pack('128sI', str(os.path.basename(file_path)), os.stat(file_path).st_size)
                client_socket.send(fhead)
                # with open(filepath,'rb') as fo: 这样发送文件有问题，发送完成后还会发一些东西过去
                fo = open(file_path, 'rb')
                while True:
                    filedata = fo.read(1024)
                    if not filedata:
                        break
                    client_socket.send(filedata)
                fo.close()
                close(client_socket)
                logger.info('send file %s finished' % file_path)
            try:
                os.system('rm -rf %s' % file_path)
            except Exception as e:
                logger.error(e)
                try:
                    os.remove(file_path)
                except Exception as e:
                    logger.error(e)
    except Exception as e:
        logger.error(e)
        logger.error('send file %s failed' % file_path)

if __name__ == '__main__':
    mq_obj = consumer.mq_consumer()
    mq_obj.init_consumer(sendf)
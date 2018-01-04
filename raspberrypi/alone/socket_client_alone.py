# -*- coding: utf-8 -*-
import os
import socket
import struct
from optparse import OptionParser
try:
    from raspberrypi.setting import HOST,PORT
except Exception:
    from setting import HOST,PORT
import hashlib
from rabbitmq_util import consumer


def connect():
    remote_ip = HOST
    port = PORT
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(2)
    try:
        client_socket.connect((remote_ip, port))
    except Exception as e:
        print('Unable to connect because of %s' % e)
        return None
    else:
        print('Connected to remote host. Start sending messages')
        return client_socket


def close(client_socket):
    try:
        client_socket.close()
    except Exception as e:
        print('Unable to deconnect because of %s' % e)
        return False
    else:
        print('DeConnected to remote host. Start sending messages')
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
                print('start send file %s length %s md5 %s' % (file_path, os.stat(file_path).st_size, md5))
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
                print('send file %s finished' % file_path)
    except Exception as e:
        print(e)
        print('send file %s failed' % file_path)

if __name__ == '__main__':
    mq_obj = consumer.mq_consumer()
    mq_obj.init_consumer(sendf)
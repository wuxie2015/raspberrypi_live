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

class SocketClient:
    def __init__(self,remote_ip,port):
        self.remote_ip = remote_ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)
        self.connect()

    def connect(self):
        try:
            self.client_socket.connect((self.remote_ip, self.port))
        except Exception as e:
            print('Unable to connect because of %s'%e)
        else:
            print('Connected to remote host. Start sending messages')

    def close(self):
        try:
            self.client_socket.close()
            del self.client_socket
        except Exception as e:
            print('Unable to connect because of %s'%e)
        else:
            print('Connected to remote host. Start sending messages')

    def calc_md5(self,f_name):
        with open(f_name, 'rb') as fr:
            md5 = hashlib.md5()
            md5.update(fr.read())
            md5 = md5.hexdigest()
        return md5

    def sendf(self,file_path):
        try:
            self.connect()
            if os.path.isfile(file_path):
                fileinfo_size = struct.calcsize('128sI')  # 定义打包规则
                # 定义文件头信息，包含文件名和文件大小
                md5 = self.calc_md5(file_path)
                md5 = md5.encode('utf8')
                f_name_bytes = os.path.basename(file_path).encode('utf8')
                f_name_length = len(f_name_bytes)
                fhead = struct.pack('128sII32s', f_name_bytes, f_name_length, os.stat(file_path).st_size, md5)
                print('start send file %s length %s md5 %s'%(file_path,os.stat(file_path).st_size,md5))
                # fhead = struct.pack('128sI', str(os.path.basename(file_path)), os.stat(file_path).st_size)
                self.client_socket.send(fhead)
                # with open(filepath,'rb') as fo: 这样发送文件有问题，发送完成后还会发一些东西过去
                fo = open(file_path, 'rb')
                while True:
                    filedata = fo.read(1024)
                    if not filedata:
                        break
                    self.client_socket.send(filedata)
                fo.close()
                self.close()
                print('send file %s finished'%file_path)
        except Exception as e:
            print(e)
            print('reconnect now')
            # self.close()
            print('send file %s failed' % file_path)

if __name__ == '__main__':
    sc_obj = SocketClient(HOST,PORT)
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file", help="File", metavar="File")
    (options, args) = parser.parse_args()
    file = options.file
    sc_obj.sendf(file)

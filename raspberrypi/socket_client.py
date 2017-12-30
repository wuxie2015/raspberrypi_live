# -*- coding: utf-8 -*-
import os
import socket
import struct
from setting import HOST,PORT

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
        except Exception,e:
            print 'Unable to connect because of %s'%e
        else:
            print 'Connected to remote host. Start sending messages'

    def sendf(self,file_path):
        if os.path.isfile(file_path):
            fileinfo_size = struct.calcsize('128sI')  # 定义打包规则
            # 定义文件头信息，包含文件名和文件大小
            print(file_path)
            fhead = struct.pack('128sI', str(os.path.basename(file_path)), os.stat(file_path).st_size)
            print(len(fhead))
            self.client_socket.send(fhead)
            # with open(filepath,'rb') as fo: 这样发送文件有问题，发送完成后还会发一些东西过去
            fo = open(file_path, 'rb')
            while True:
                filedata = fo.read(1024)
                if not filedata:
                    break
                self.client_socket.send(filedata)
            fo.close()

if __name__ == '__main__':
    sc_obj = SocketClient(HOST,PORT)
    sc_obj.sendf('output.avi')
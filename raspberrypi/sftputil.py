# -*- coding: utf-8 -*-
import paramiko


class SftpUtil(object):
    def __init__(self, ip, username, password, timeout=30):
        self.ip = ip
        self.username = username
        self.passowrd = password
        self.chan = ''
        # 链接失败的重试次数
        self.try_times = 3
        self.connect()

    def connect(self):
        self.t = paramiko.Transport(sock= (self.ip, 22))
        self.t.connect(username=self.username, password=self.passowrd)
        self.sftp =  paramiko.SFTPClient.from_transport(self.t)

    def close(self):
        self.sftp.close()
        del self.t

    def put(self,file_path):
        self.sftp.put(file_path, '/usr/local/project/tmp_video/%s'%file_path)

    def get(self,local_file_path,remote_file_path):
        self.sftp.get(remote_file_path,local_file_path)

if __name__ == '__main__':
    sftp_obj = SftpUtil('118.126.65.199','root','Csu@2012')
    sftp_obj.put('output.avi')
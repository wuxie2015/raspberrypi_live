#-*- coding: UTF-8 -*-
try:
    from server.rabbitmq_util import producer
except ModuleNotFoundError:
    from rabbitmq_util import producer
import socketserver
import struct
import os
import hashlib

host = '0.0.0.0'
port = 12306
ADDR = (host, port)

BUFFER_SIZE = 4*1024


class MyRequestHandler(socketserver.BaseRequestHandler):
    # def __init__(self, request, client_address, server):
    #     socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
    #     self.mq_obj = producer.mq_producer()

    def calc_md5(self,f_name):
        with open(f_name, 'rb') as fr:
            md5 = hashlib.md5()
            md5.update(fr.read())
            md5 = md5.hexdigest()
        return md5

    def handle(self):
        mq_obj = producer.mq_producer()
        print('connected from:', self.client_address)
        # 定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
        fileinfo_size = struct.calcsize('128sII32s')
        self.buf = self.request.recv(fileinfo_size)
        if self.buf:  # 如果不加这个if，第一个文件传输完成后会自动走到下一句
            try:
                filename, filenamesize, filesize, md5 = struct.unpack(
                    '128sII32s', self.buf)  # 根据128sII32s解包文件信息，与client端的打包规则相同
            except struct.error as e:
                print(e)
                self.request.close()
                return
            try:
                filesize = int(filesize)
                # 文件名长度为128，大于文件名实际长度
                filename = filename[:filenamesize]
                md5 = md5.decode('utf8')
                print('notified that file name %s file size %s file md5 %s' % (filename, filesize, md5))
                filenewname = os.path.join(
                    '/usr/local/project/tmp_video/',
                    ('new_' + filename.decode('utf8')).strip('\00').strip('\\x00'))  # 使用strip()删除打包时附加的多余空字符
            except Exception as e:
                print(e)
                print("error in %s" % filename)
                while True:  # 清空缓冲区
                    buf = self.request.recv(BUFFER_SIZE)
                    if not len(buf):
                        break
                self.request.close()  # 出现错误宁愿丢弃文件也不能影响程序运行
                return
            try:
                print("ready to receive %s" % filenewname)
                recvd_size = 0  # 定义接收了的文件大小
                file = open(filenewname, 'wb')
                print('start receiving...')
                while not recvd_size == filesize:
                    if filesize - recvd_size > BUFFER_SIZE:
                        rdata = self.request.recv(BUFFER_SIZE)
                        recvd_size += len(rdata)
                    else:
                        rdata = self.request.recv(BUFFER_SIZE)
                        # rdata = self.request.recv(filesize - recvd_size)
                        recvd_size = filesize
                    file.write(rdata)
                file.close()
                md5_recv = self.calc_md5(filenewname)
                if md5_recv == md5:
                    print('receive done')
                    mq_obj.put_message(filenewname)
                else:
                    print('md5 do not match')
            except Exception as e:
                print(e)
                print("file %s recieve failed" % filenewname)
                self.request.close()
                return
        self.request.close()


tcpServ = socketserver.ThreadingTCPServer(ADDR, MyRequestHandler)
print('waiting for connection...')
tcpServ.serve_forever()

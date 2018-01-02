#-*- coding: UTF-8 -*-
import threading
from server.socket_server import MyRequestHandler
from server.scan_file import scan_queue_file
from server.rabbitmq_util import consumer
import socketserver

host = '0.0.0.0'
port = 12306
ADDR = (host, port)


class ReceiveFile(threading.Thread):
    def __init__(self, t_name):
        threading.Thread.__init__(self, name=t_name)
        self.stopped = False
        self.tcpServ = socketserver.ThreadingTCPServer(ADDR, MyRequestHandler)

    def run(self):
        self.tcpServ.serve_forever()


class ProcessFile(threading.Thread):
    def __init__(self, t_name):
        threading.Thread.__init__(self, name=t_name)
        self.stopped = False
        self.mq_obj = consumer.mq_consumer()

    def run(self):
        self.mq_obj.init_consumer(scan_queue_file)


def test():
    thread1 = ReceiveFile('ReceiveFile')
    thread2 = ProcessFile('ProcessFile')
    thread1.start()
    thread2.start()


if __name__ == '__main__':
    test()

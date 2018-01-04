#-*- coding: UTF-8 -*-
import socket, select, string, sys
from .Queue import Queue
import threading

HOST = '127.0.0.1'
PORT = 5247

class MQListener(threading.Thread):
    def __init__(self,id,password,queue_obj):
        threading.Thread.__init__(self)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)
        self.id = id
        self.password = password
        self.connect()
        self.queue = queue_obj

    def connect(self):
        try:
            self.client_socket.connect((HOST, PORT))
            self.client_socket.send("%s||%s"%(self.id,self.password))
        except Exception as e:
            print('Unable to connect because of %s'%e)
            sys.exit()
        else:
            print('Connected to remote host. Start sending messages')

    def basic_producer(self,data):
        remote_id = "all"
        msg_send = "%s||%s" % (remote_id, data)
        self.client_socket.send(msg_send)

    def socket_handler(self):
        while 1:
            rlist = [self.client_socket]  # 接收列表
            read_list, write_list, error_list = select.select(rlist, [], [], 2)
            for sock in read_list:
                # incoming message from remote server
                if sock == self.client_socket:
                    data = sock.recv(4096)
                    if not data:
                        print('\nDisconnected from chat server')
                        self.connect()
                    else:
                        # print data
                        sys.stdout.write(data)
                        self.queue.put(data)

    def run(self):
        self.socket_handler()

class MQClient(threading.Thread):
    def __init__(self,queue_obj):
        threading.Thread.__init__(self)
        self.queue = queue_obj

    def basic_consumer(self,call_back):
        self.call_back = call_back

    def run(self):
        while True:
            while self.queue.empty():
                pass
            data = self.queue.get()
            self.call_back(data)

def test():
    queue = Queue(10000)
    thread_listener = MQListener('2','123456',queue)
    thread_client = MQClient(queue)
    thread_listener.start()
    thread_client.start()

if __name__ == '__main__':
    test()
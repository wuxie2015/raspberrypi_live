# -*- coding:utf-8 -*-
import socket
import select
import sys
from optparse import OptionParser
from setting import HOST,PORT
import time
import signal
import logging
from logging.handlers import RotatingFileHandler

def time_limit(interval):
    def wraps(func):
        def handler(*args, **kwargs):
            raise RuntimeError()

        def deco(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(interval)
            res = func(*args, **kwargs)
            signal.alarm(0)
            return res
        return deco
    return wraps

class ChatClient:
    def __init__(self, id, password):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)
        self.id = id
        self.password = password
        self.logger = self.logger_init()

    def logger_init(self):
        # 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
        log_file = 'tri_body_yewenjie.log'
        Rthandler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
        Rthandler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('\n%(asctime)s   %(filename)s[line:%(lineno)d]   %(levelname)s\n%(message)s')
        Rthandler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.addHandler(Rthandler)
        logger.setLevel(logging.DEBUG)
        return logger

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)
        try:
            self.client_socket.connect((HOST, PORT))
            message = "%s||%s" % (self.id, self.password)
            self.client_socket.send(message)
        except Exception as e:
            self.logger.error('Unable to connect because of %s' % e)
            sys.exit()
        else:
            self.logger.info('Connected to remote host. Start sending messages')
            self.prompt()

    def prompt(self):
        sys.stdout.write('\n<You> ')
        sys.stdout.flush()

    def connect_program(self):
        try:
            self.client_socket.connect((HOST, PORT))
            message = "%s||%s" % (self.id, self.password)
            self.client_socket.send(message)
        except Exception as e:
            self.logger.error('Unable to connect because of %s' % e)
        else:
            self.logger.info('Connected to remote host. Start sending messages')

    def reconnect(self):
        self.client_socket.close()
        del self.client_socket
        time.sleep(10)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)
        self.connect_program()

    def send_once(self, msg, remote_id):
        self.logger.info("send %s to %s"%(msg,remote_id))
        msg_send = "%s||%s" % (remote_id, msg)
        self.client_socket.send(msg_send)

    def socket_handler(self,callback_func=None):
        while True:
            rlist = [sys.stdin, self.client_socket]  # 接收列表
            read_list, write_list, error_list = select.select(rlist, [], [], 2)
            for sock in read_list:
                # incoming message from remote server
                if sock == self.client_socket:
                    data = sock.recv(4096)
                    if not data:
                        self.logger.error('Disconnected from chat server')
                        self.reconnect()
                    else:
                        if callback_func is None:
                            sys.stdout.write(data)
                            self.prompt()
                        else:
                            callback_func(data)

                # user entered a message
                else:
                    msg = sys.stdin.readline()
                    remote_id = input("Please input remote id:")
                    msg_send = "%s||%s" % (remote_id, msg)
                    self.client_socket.send(msg_send)
                    self.prompt()

    @time_limit(1200)
    def socket_handler_program(self,callback_func=None):
        while True:
            rlist = [self.client_socket]  # 接收列表
            read_list, write_list, error_list = select.select(rlist, [], [], 2)
            for sock in read_list:
                # incoming message from remote server
                if sock == self.client_socket:
                    data = sock.recv(4096)
                    if not data:
                        self.logger.error('Disconnected from chat server')
                        self.reconnect()
                    else:
                        if callback_func is None:
                            sys.stdout.write(data)
                            self.prompt()
                        else:
                            callback_func(self,data)

                # user entered a message
                else:
                    self.logger.error('invalid input detected')

    def recieve_echo(self,timeout=60):
        data = 'initial data'
        start = time.time()
        now = time.time()
        while not data and (now - start) < int(timeout):
            data = self.client_socket.recv(4096)
            now = time.time()
            if data:
                print('echo data %s'%data)
                self.logger.info('echo data %s'%data)

    def close(self):
        self.client_socket.close()


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--id", dest="id", help="Chat id", metavar="ID")
    parser.add_option(
        "-p",
        "--password",
        dest="password",
        help="Password",
        metavar="PASSWORD")
    (options, args) = parser.parse_args()
    if options.id is None:
        parser.error("please input the id")
    if options.password is None:
        parser.error("please input the password")
    id = options.id
    password = options.password
    chat_client_obj = ChatClient(id, password)
    chat_client_obj.connect()
    chat_client_obj.socket_handler()

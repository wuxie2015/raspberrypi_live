# -*- coding:utf-8 -*-
import socket, select, string, sys
from optparse import OptionParser
HOST = '127.0.0.1'
PORT = 5247

class ChatClient:
    def __init__(self,id,password):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)
        self.id = id
        self.password= password
        self.connect()

    def connect(self):
        try:
            self.client_socket.connect((HOST, PORT))
            self.client_socket.send("%s||%s"%(self.id,self.password))
        except Exception as e:
            print('Unable to connect because of %s'%e)
            sys.exit()
        else:
            print('Connected to remote host. Start sending messages')
            self.prompt()


    def prompt(self):
        sys.stdout.write('\n<You> ')
        sys.stdout.flush()

    def socket_handler(self):
        while 1:
            rlist = [sys.stdin, self.client_socket]  # 接收列表
            read_list, write_list, error_list = select.select(rlist, [], [], 2)
            for sock in read_list:
                # incoming message from remote server
                if sock == self.client_socket:
                    data = sock.recv(4096)
                    if not data:
                        print('\nDisconnected from chat server')
                        sys.exit()
                    else:
                        # print data
                        sys.stdout.write(data)
                        self.prompt()

                # user entered a message
                else:
                    msg = sys.stdin.readline()
                    remote_id = input("Please input remote id:")
                    msg_send = "%s||%s"%(remote_id,msg)
                    self.client_socket.send(msg_send)
                    self.prompt()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--id", dest="id", help="Chat id", metavar="ID")
    parser.add_option("-p", "--password", dest="password", help="Password", metavar="PASSWORD")
    (options, args) = parser.parse_args()
    if options.id == None:
        parser.error("please input the id")
    if options.password == None:
        parser.error("please input the password")
    id = options.id
    password = options.password
    chat_client_obj = ChatClient(id,password)
    chat_client_obj.socket_handler()
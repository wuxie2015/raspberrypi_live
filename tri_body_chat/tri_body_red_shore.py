# -*- coding: utf-8 -*-
import select
import socket
import threading

inBufSize = 4096
outBufSize = 4096
CONNECTION_LIST = []
PASSWORD = '123456'#先暂时设置一个，以后放到数据库里

class ChatServer(threading.Thread):
    def __init__(self,port=5247):
        threading.Thread.__init__(self)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(('', port))
        self.serverSocket.listen(5)
        print "server wait for connect...."
        self.socketsMap = {}  # socket session字典 id : socket
        self.idMap = {} #socket session 字典 socket:id
        CONNECTION_LIST.append(self.serverSocket)

    def auth(self,password):
        if password == PASSWORD:
            return 0
        else:
            return 1#0登录成功1登录失败

    def login(self,login_data,sock):#新用户登录
        try:
            id = login_data.split('||')[0]
            password = login_data.split('||')[1]
        except IndexError, e:
            print login_data
            print e
        else:
            auth_result = self.auth(password)
            if auth_result == 0:
                print "%s login"%id
                self.socketsMap[id] = sock
                self.idMap[sock] = id
                sock.send('hello %s,you login successed'%id)
                CONNECTION_LIST.append(sock)#要在这里把socket加进来才行
            else:
                sock.send("Password inncorrect")

    def chat(self,sock):#点对点聊天，发送消息格式id||信息
        try:
            data = sock.recv(inBufSize)
        except Exception:
            print "sender is offline"
            sock.close()
        else:
            if data == '':
                sender_id = self.idMap[sock]
                print "%s is offline"%sender_id
                CONNECTION_LIST.remove(sock)
                sock.close()
                return 0
            try:
                remote_id = data.split('||')[0]
                message = data.split('||')[1]
            except IndexError,e:
                print data
                print e
            else:
                print "id = %s,message = %s"%(remote_id,message)
                local_id = self.idMap[sock]
                if remote_id == 'all':
                    self.broadcast(local_id,message)
                else:
                    self.p2psend(local_id,message,remote_id)

    def p2psend(self,local_id,message,remote_id):
        try:
            remote_socket = self.socketsMap[remote_id]
        except KeyError:
            local_socket = self.socketsMap[local_id]
            local_socket.send("remote %s is offline"%remote_id)
        else:
            message_send = "%s said : %s" % (local_id, message)
            try:
                remote_socket.sendall(message_send)
            except Exception,e:
                print e
                remote_socket.close()
                CONNECTION_LIST.remove(remote_socket)

    def broadcast(self,local_id,message):
        for sock in CONNECTION_LIST:
            if sock == self.serverSocket:
                continue
            else:
                try:
                    message_send = "%s said : %s" % (local_id, message)
                    sock.send(message_send)
                except Exception,e:
                    print e
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

    def socet_handle(self):
        while 1:
            # Get the list sockets which are ready to be read through select
            try:
                read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])
            except:
                continue
            for sock in read_sockets:
                # New connection
                if sock == self.serverSocket:#用户通过主socket（即服务器开始创建的 socket，一直处于监听状态）来登录
                    # Handle the case in which there is a new connection recieved through server_socket
                    sockfd, addr = self.serverSocket.accept()
                    login_data = sockfd.recv(100)
                    self.login(login_data,sockfd)
                else:
                    self.chat(sock)

    def run(self):
        self.socet_handle()
        self.serverSocket.close()

if __name__ == '__main__':
    chat_server_obj = ChatServer()
    chat_server_obj.start()
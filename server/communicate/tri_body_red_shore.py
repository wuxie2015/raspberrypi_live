# -*- coding: utf-8 -*-
import select
import socket
import threading
from setting import PASSWORD,PORT
import logging
from logging.handlers import RotatingFileHandler

inBufSize = 4096
outBufSize = 4096
CONNECTION_LIST = []


class ChatServer(threading.Thread):
    def __init__(self, port=PORT):
        threading.Thread.__init__(self)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(('', port))
        self.serverSocket.listen(5)
        print("server wait for connect....")
        self.socketsMap = {}  # socket session字典 id : socket
        self.idMap = {}  # socket session 字典 socket:id
        CONNECTION_LIST.append(self.serverSocket)
        self.logger = self.logger_init()

    def logger_init(self):
        # 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
        log_file = 'tri_body_red_shore.log'
        Rthandler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
        Rthandler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('\n%(asctime)s   %(filename)s[line:%(lineno)d]   %(levelname)s\n%(message)s')
        Rthandler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.addHandler(Rthandler)
        logger.setLevel(logging.DEBUG)
        return logger

    def auth(self, password):
        if password == PASSWORD or ("b'" + password + "'") == PASSWORD:
            return 0
        else:
            return 1  # 0登录成功1登录失败

    def login(self, login_data, sock):  # 新用户登录
        try:
            if isinstance(login_data, bytes):
                login_data = login_data.decode('utf8')
            id = login_data.split('||')[0]
            password = login_data.split('||')[1]
        except IndexError as e:
            print(login_data)
            print('error in login %s'%e)
            self.logger.error(login_data)
            self.logger.error('error in login %s'%e)
            raise ValueError('list is empty')
        else:
            auth_result = self.auth(password)
            if auth_result == 0:
                print("%s login" % id)
                self.logger.info("%s login" % id)
                self.socketsMap[id] = sock
                self.idMap[sock] = id
                sock.send(('hello %s,you login successed' % id).encode('utf8'))
                CONNECTION_LIST.append(sock)  # 要在这里把socket加进来才行
            else:
                print('%s login failed'%id)
                self.logger.error('%s login failed'%id)
                sock.send(("Password inncorrect").encode('utf8'))

    def chat(self, sock):  # 点对点聊天，发送消息格式id||信息
        try:
            data = sock.recv(inBufSize)
        except Exception:
            print("sender is offline")
            self.logger.warning("sender is offline")
            CONNECTION_LIST.remove(sock)
            self.idMap.pop(sock)
            sock.close()
        else:
            if isinstance(data, bytes):
                data = data.decode('utf8')
            if data == '':
                sender_id = self.idMap[sock]
                print("%s is offline" % sender_id)
                self.logger.warning("%s is offline" % sender_id)
                CONNECTION_LIST.remove(sock)
                self.idMap.pop(sock)
                sock.close()
                return 0
            try:
                remote_id = data.split('||')[0]
                message = data.split('||')[1]
            except IndexError as e:
                print("error in chat %s and data is %s"%(e,data))
                self.logger.error("error in chat %s and data is %s"%(e,data))
                raise ValueError('list out of range')
            else:
                print("id = %s,message = %s" % (remote_id, message))
                self.logger.info("id = %s,message = %s" % (remote_id, message))
                local_id = self.idMap[sock]
                if remote_id == 'all':
                    self.broadcast(local_id, message)
                else:
                    self.p2psend(local_id, message, remote_id)

    def p2psend(self, local_id, message, remote_id):
        try:
            remote_socket = self.socketsMap[remote_id]
        except KeyError:
            local_socket = self.socketsMap[local_id]
            local_socket.send(
                ("remote %s is offline" %
                 remote_id).encode('utf8'))
        else:
            message_send = "%s||%s" % (local_id, message)
            try:
                remote_socket.sendall(message_send.encode('utf8'))
            except Exception as e:
                print("Error in p2psend %s"%e)
                self.logger.error("Error in p2psend %s"%e)
                remote_socket.close()
                CONNECTION_LIST.remove(remote_socket)
                self.idMap.pop(remote_socket)

    def broadcast(self, local_id, message):
        for sock in CONNECTION_LIST:
            if sock == self.serverSocket:
                continue
            else:
                try:
                    message_send = "%s||%s" % (local_id, message)
                    sock.send(message_send.encode('utf8'))
                except Exception as e:
                    print("Error in broadcast %s"%e)
                    self.logger.error("Error in broadcast %s"%e)
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    self.idMap.pop(sock)
                    continue

    def socet_handle(self):
        while True:
            # Get the list sockets which are ready to be read through select
            try:
<<<<<<< HEAD
                read_sockets, write_sockets, error_sockets = select.select(
                    CONNECTION_LIST, [], [])
            except BaseException as e:
                print("Error in socket_handle %s"%e)
                self.logger.error("Error in socket_handle %s"%e)
                continue
            for sock in read_sockets:
                # New connection
                if sock == self.serverSocket:  # 用户通过主socket（即服务器开始创建的 socket，一直处于监听状态）来登录
                    # Handle the case in which there is a new connection
                    # recieved through server_socket
                    sockfd, addr = self.serverSocket.accept()
                    login_data = sockfd.recv(100)
                    try:
                        self.login(login_data, sockfd)
                    except ValueError:
                        break
                else:
                    try:
                        self.chat(sock)
                    except ValueError:
                        continue
=======
                try:
                    read_sockets, write_sockets, error_sockets = select.select(
                        CONNECTION_LIST, [], [])
                except BaseException as e:
                    print("Error in socket_handle %s"%e)
                    self.logger.error("Error in socket_handle %s"%e)
                    continue
                for sock in read_sockets:
                    # New connection
                    if sock == self.serverSocket:  # 用户通过主socket（即服务器开始创建的 socket，一直处于监听状态）来登录
                        # Handle the case in which there is a new connection
                        # recieved through server_socket
                        sockfd, addr = self.serverSocket.accept()
                        login_data = sockfd.recv(100)
                        try:
                            self.login(login_data, sockfd)
                        except ValueError:
                            break
                    else:
                        try:
                            self.chat(sock)
                        except ValueError:
                            continue
            except BaseException as e:
                print("Error in socket_handle %s" % e)
                self.logger.error("Error in socket_handle %s" % e)
>>>>>>> bc2ebfe5aed7998f7b62599c1143004cc214b7e5

    def run(self):
        self.socet_handle()
        self.serverSocket.close()


if __name__ == '__main__':
    chat_server_obj = ChatServer()
    chat_server_obj.start()

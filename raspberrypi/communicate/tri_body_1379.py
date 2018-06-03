# -*- coding:utf-8 -*-
from tri_body_yewenjie import ChatClient
from setting import PASSWORD


class ChatUser:
    def __init__(self):
        pass

    def process(self,msg='open led',remote_id='1'):
        chat_obj = ChatClient('0', PASSWORD)
        chat_obj.connect_program()
        chat_obj.send_once(msg, remote_id)
        chat_obj.recieve_echo()
        chat_obj.close()


if __name__ == '__main__':
    chat_test_obj = ChatUser()
    chat_test_obj.process()
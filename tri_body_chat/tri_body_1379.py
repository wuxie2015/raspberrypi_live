# -*- coding:utf-8 -*-
from tri_body_yewenjie import ChatClient

class ChatTest:
    def __init__(self):
        pass

    def process(self):
        test_list = []
        for i in range(1,200+1):
            chat_client_obj = ChatClient(str(i),'123456')
            test_list.append(chat_client_obj)

if __name__ == '__main__':
    chat_test_obj = ChatTest()
    chat_test_obj.process()
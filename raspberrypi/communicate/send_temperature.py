# -*- coding:utf-8 -*-
from tri_body_yewenjie import ChatClient
from setting import PASSWORD
from cmd_util import get_temperature
import json


class ChatUser:
    def __init__(self):
        self.channel = 29

    def get_temperature(self):
        temperature_result = get_temperature.main(self.channel)
        result_json = json.dumps(temperature_result)
        return result_json

    def process(self,remote_id='1'):
        msg = self.get_temperature()
        chat_obj = ChatClient('0', PASSWORD)
        chat_obj.connect_program()
        chat_obj.send_once(msg, remote_id)
        chat_obj.recieve_echo()
        chat_obj.close()

if __name__ == '__main__':
    chat_test_obj = ChatUser()
    chat_test_obj.process()
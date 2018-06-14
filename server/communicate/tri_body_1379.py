#! /usr/bin/python
# -*- coding:utf-8 -*-
from tri_body_yewenjie import ChatClient
from setting import HOST,PORT
from optparse import OptionParser


class ChatUser:
    def __init__(self):
        pass

    def process_command(self,command):
        if command == 'reboot':
            self.process(command='0')
        elif command == 'start camera':
            self.process(command='1',timeout=60)
        elif command == 'restart camera':
            self.process(command='2',timeout=60)
        elif command == 'close camera':
            self.process(command='3')
        elif command == 'check camera':
            self.process(command='4')
        elif command == 'test':
            self.process(command='100')
        else:
            print('invalid data')

    def process(self,command='open led',remote_id='0',timeout=5):
        msg = command
        remote_id = remote_id
        chat_obj = ChatClient('1', '123456')
        chat_obj.connect_program()
        chat_obj.send_once(msg, remote_id)
        try:
            chat_obj.recieve_echo(timeout=timeout)
        except RuntimeError:
            pass
        chat_obj.close()


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--command", dest="command", help="Chat command", metavar="COMMAND")
    parser.add_option(
        "-r",
        "--remote_id",
        dest="remote_id",
        help="remote id",
        metavar="REMOTE_ID")
    (options, args) = parser.parse_args()
    if options.command is None:
        parser.error("please input the command")
    # if options.password is None:
    #     parser.error("please input the password")
    command = options.command
    chat_test_obj = ChatUser()
    chat_test_obj.process_command(command= command)

# !/usr/bin/env python
import pika
from setting import HOST,PORT,RABBIT_USER,RABBIT_PASSWORD

class mq_producer:
    def __init__(self):
        credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = HOST, port = 5672,
                                                                            virtual_host = 'raspberry', credentials =credentials,
                                                                            heartbeat_interval = 0))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='file_queue')

    def put_message(self,massage):
        self.channel.basic_publish(exchange='',
                      routing_key='file_queue',
                      body=massage)

    def close(self):
        self.channel.close()
        self.connection.close()
if __name__ == '__main__':
    mq_obj = mq_producer()
    mq_obj.put_message('output.avi')

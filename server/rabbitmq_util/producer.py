# !/usr/bin/env python
import pika

class mq_producer:
    def __init__(self):
        credentials = pika.PlainCredentials('admin', '123456')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = '127.0.0.1', port = 5672,
                                                                            virtual_host = '/', credentials =credentials,
                                                                            heartbeat_interval = 1200))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='file_queue')

    def put_message(self,massage):
        self.channel.basic_publish(exchange='',
                      routing_key='file_queue',
                      body=massage)
if __name__ == '__main__':
    mq_obj = mq_producer()
    mq_obj.put_message('output.avi')

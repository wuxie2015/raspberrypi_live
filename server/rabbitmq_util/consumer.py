# !/usr/bin/env python
import pika

class mq_consumer:
    def __init__(self):
        credentials = pika.PlainCredentials('admin', '123456')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = '127.0.0.1', port = 5672,
                                                                            virtual_host = '/', credentials =credentials,
                                                                            heartbeat = 0))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='file_queue')

    def init_consumer(self,callback_func):
        self.channel.basic_consume(callback_func,
                              queue='file_queue',
                              no_ack=True)
        self.channel.start_consuming()

def test_callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

if __name__ == '__main__':
    mq_obj = mq_consumer()
    mq_obj.init_consumer(test_callback)
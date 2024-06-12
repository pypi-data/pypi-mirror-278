import logging
import pika
import json
import os
from datetime import datetime
class AMQPLoggingHandler(logging.Handler):
    def __init__(self,amqp_url=None, queue_name=None,msg_priority=10,*args, **kwargs):
        super().__init__()
        self.amqp_url = os.environ.get('AMQP_URL', amqp_url)
        self.queue_name = os.environ.get('QUEUE_NAME', queue_name)
        self.msg_priority = msg_priority
        self.priority_q = {"x-max-priority": self.msg_priority}
        self.connection = None
        self.channel = None
        print('Initialising AMQPHandler with url: {} and key: {}'.format(self.amqp_url, self.queue_name))

    def _connect(self):
        self.params = pika.URLParameters(self.amqp_url)
        self.params.socket_timeout = 1300
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, arguments = self.priority_q)

    def emit(self, record):
        try:
            if not self.channel or self.channel.is_closed:
                self._connect()

            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(json.dumps(record.args)),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                    priority=self.msg_priority
                )
            )
        except Exception:
            self.handleError(record)

    def close(self):
        if self.channel:
            self.channel.close()
        if self.connection:
            self.connection.close()
        super().close()

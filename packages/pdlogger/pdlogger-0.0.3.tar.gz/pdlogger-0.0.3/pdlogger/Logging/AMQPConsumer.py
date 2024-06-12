import pika
import json
import os
from .MysqlDBUtils import MySQLDatabase


class AMQPConsumer:
    def __init__(self, amqp_url=None, queue_name=None, sql_host=None, sql_user=None, sql_password=None, sql_database=None):
        self.url = os.environ.get('AMQP_URL', amqp_url)
        self.deploy_queue = os.environ.get('QUEUE_NAME', queue_name)
        self.db_config = {
            'host': os.environ.get('SQL_HOST', sql_host),
            'user': os.environ.get('SQL_USER', sql_user),
            'password': os.environ.get('SQL_PASSWORD', sql_password),
            'database': os.environ.get('SQL_DATABASE', sql_database)
        }
        self.params = pika.URLParameters(self.url)
        self.params.socket_timeout = 1300
        self.connection = None
        self.channel = None

    def logs_insert(self, input_data):
        print("Inserting into database")
        input_data = json.loads(input_data)
        insert_query = input_data["insert_query"]
        insert_values = input_data['insert_values']
        db = MySQLDatabase(**self.db_config)
        return_msg = db.insert_data(insert_query, insert_values)
        print(return_msg)

    def callback(self, ch, method, properties, body):
        input_data = json.loads(body.decode("utf-8"))
        print("Received data--->", input_data)
        try:
            self.logs_insert(input_data)
        except Exception as e:
            print(e)
        print("Consumed")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        while True:
            try:
                self.connection = pika.BlockingConnection(self.params)
                self.channel = self.connection.channel()
                priority_q = {"x-max-priority": 10}
                self.channel.queue_declare(queue=self.deploy_queue, arguments=priority_q, durable=False)
                self.channel.basic_qos(prefetch_count=1)
                print(self.deploy_queue)
                self.channel.basic_consume(self.callback,queue=self.deploy_queue)
                print(f"[*] Started consuming on queue: {self.deploy_queue}")
                self.channel.start_consuming()
            except Exception as e:
                print(e)
                print(" [*] Restarting listening")

if __name__ == '__main__':
    consumer = LogConsumer()
    consumer.start_consuming()

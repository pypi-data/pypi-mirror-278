#encoding=utf-8
import pika
import logging,traceback

class RabbitMQ:
    def __init__(self,mq_settings):
        self.settings=mq_settings
        self.conn=None

    def __connect(self):
        if self.conn is None:
            credentials = pika.PlainCredentials(self.settings.account, self.settings.password)
            self.conn=pika.BlockingConnection(pika.ConnectionParameters(self.settings.host,self.settings.port,'/',credentials))

    def send_msg(self,exchange,routing_key,message):
        try:
            self.__connect()
            channel = self.conn.channel()
            #channel.exchange_declare(exchange=exchange, durable=True, exchange_type='fanout')
            #channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message,  mandatory=True,properties=pika.BasicProperties(delivery_mode = 2))

            channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
            self.conn.close()
            self.conn = None
            return 200
        except Exception as e:
            traceback.print_exc()
            logging.warning(e,'while sending message to exchange: {} with key: {}'.format(exchange,routing_key))
            try:
                self.conn.close()
            finally:
                self.conn=None
                return 500


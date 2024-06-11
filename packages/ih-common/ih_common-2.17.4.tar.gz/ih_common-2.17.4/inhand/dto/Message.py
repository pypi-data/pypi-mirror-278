import json
from inhand.service.MQSender import RabbitMQ

class PushMessage:
    locale: str = "English"
    title: str = None
    short_content: str = None
    content: str = None
    app_tag_list: list = []
    app_alias_list: list = []
    audience: str = None
    phone_list: list = []
    email_list: list = []
    im_list: list = []
    params: dict = {}

    def __init__(self):
        pass

    def toDict(self):
        kv= {
            'locale': self.locale,
            'title': self.title,
            'short_content': self.short_content,
            'content': self.content,
            'app_tag_list': self.app_tag_list,
            'app_alias_list': self.app_alias_list,
            'audience': self.audience,
            'phone_list': self.phone_list,
            'email_list': self.email_list,
            'im_list': self.im_list,
            'params': self.params
        }
        return kv

    def toJson(self):
        return json.dumps(self.toDict())

    def send(self,mq_sender: RabbitMQ, exchange:str, routing_key:str):
        mq_sender.send_msg(exchange,routing_key,self.toJson())


if __name__ == '__main__':
    message = PushMessage()
    message.title = "Test"
    print(message.toJson())
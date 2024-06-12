import json
import time
from channels.generic.websocket import WebsocketConsumer


class Consumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print(self.scope["user"])
        # self.close()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        self.send(text_data=text_data)
        self.close()

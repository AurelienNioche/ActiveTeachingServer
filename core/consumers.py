from channels.generic.websocket import WebsocketConsumer
import json

from core.q_and_a import get_question


class WebSocketConsumer(WebsocketConsumer):
    def connect(self):
        print("Connecting")
        self.accept()

    def disconnect(self, close_code):
        print(f'Disconnection! Close code: {close_code}')

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print("Receive:", text_data_json)
        # message = text_data_json['message']

        question = get_question(text_data_json)

        print("Send:", question)
        self.send(text_data=json.dumps(question))

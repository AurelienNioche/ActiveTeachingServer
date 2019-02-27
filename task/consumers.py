from channels.generic.websocket import WebsocketConsumer
import json


class WebSocketConsumer(WebsocketConsumer):

    def connect(self):

        print("Connecting")

        self.accept()

    def disconnect(self, close_code):

        print(f'Disconnection! Close code: {close_code}')

    def receive(self, text_data=None, bytes_data=None):

        print("Receive ", text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

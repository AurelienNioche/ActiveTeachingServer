from channels.generic.websocket import WebsocketConsumer
import json

from . q_and_a import get_question


class WebSocketConsumer(WebsocketConsumer):

    def connect(self):

        print("Connecting")

        self.accept()

    def disconnect(self, close_code):

        print(f'Disconnection! Close code: {close_code}')

    def receive(self, text_data=None, bytes_data=None):

        if bytes_data is not None:
            text = bytes_data.decode("utf-8")
        elif text_data is not None:
            text = text_data
        else:
            raise ValueError

        text_data_json = json.loads(text)

        print("Receive:", text_data_json)
        # message = text_data_json['message']

        question = get_question(text_data_json)

        print("Send:", question)
        resp = json.dumps(question)
        if bytes_data is not None:
            self.send(bytes_data=resp.encode())
        else:
            self.send(text_data=resp)

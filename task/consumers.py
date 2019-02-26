from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer

# import task.views

import json


class WebSocketConsumer(WebsocketConsumer):

    def connect(self):

        print("Connecting")

        self.accept()

    def disconnect(self, close_code):

        print(f'Disconnection! close code: {close_code}')
        # self._group_discard('all')

    # def receive_json(self, content, **kwargs):
    #
    #     print("Receiving json")
    #
    #     to_reply, consumer_info = task.views.client_request(content)
    #
    #     self.send_json(to_reply)
    #
    #     try:
    #         print(f'Sending to current channel: {to_reply}')
    #     except UnicodeEncodeError:
    #         print('Error printing request.')

    def receive(self, text_data):

        print("Receive ", text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

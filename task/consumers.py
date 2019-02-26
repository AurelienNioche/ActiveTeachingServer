from channels.generic.websocket import JsonWebsocketConsumer

import task.views


class WebSocketConsumer(JsonWebsocketConsumer):

    def connect(self):

        self.accept()

    def disconnect(self, close_code):

        print(f'Disconnection! close code: {close_code}')
        # self._group_discard('all')

    def receive_json(self, content, **kwargs):

        to_reply, consumer_info = task.views.client_request(content)

        self.send_json(to_reply)

        try:
            print(f'Sending to current channel: {to_reply}')
        except UnicodeEncodeError:
            print('Error printing request.')

from channels.generic.websocket import WebsocketConsumer
import json
import numpy as np

from . models import Kanjilist


class WebSocketConsumer(WebsocketConsumer):

    def connect(self):

        print("Connecting")

        self.accept()

    def disconnect(self, close_code):

        print(f'Disconnection! Close code: {close_code}')

    def receive(self, text_data=None, bytes_data=None):

        print("Receive ", text_data)
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']

        k = list(Kanjilist.objects.all())

        while True:
            idx = np.random.choice(np.arange(len(k)), size=6, replace=False)

            possible_replies = [k[idx[i]].meaning for i in range(6)]
            if len(np.unique(possible_replies)) == len(possible_replies):
                break

        question = k[idx[0]].kanji
        correct_answer = k[idx[0]].meaning

        np.random.shuffle(possible_replies)

        self.send(text_data=json.dumps({
            'question': question,
            'correctAnswer': correct_answer,
            'possibleReplies': possible_replies
        }))

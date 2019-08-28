# import requests
import json
import numpy as np

import time

import websocket


class MySocket(websocket.WebSocketApp):

    def __init__(self, url="ws://localhost:8000/",
                 n_iteration=10,
                 **kwargs):
        super().__init__(
            url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open,
            **kwargs)

        self.n_iteration = n_iteration

    def decide(self, possible_replies, **kwargs):

        return int(np.random.choice(possible_replies))

    def on_message(self, message):

        print(f"I received: {message}")
        message = json.loads(message)

        if message['t'] == -1:
            print("Done!")
            exit(0)

        id_reply = self.decide(possible_replies=message['idPossibleReplies'])
        success = id_reply == message['idCorrectAnswer']
        print("I got question", message["idQuestion"])
        print("I replied", id_reply)
        print(f"It was{' not ' if not success else ' '}a success")

        to_send = {
            'userId': message['userId'],
            'nIteration': message['nIteration'],
            'registerReplies': message['registerReplies'],
            'teacher': 'leitner',
            't': message['t'],
            'idQuestion': message["idQuestion"],
            'idCorrectAnswer': message['idCorrectAnswer'],
            'idPossibleReplies': message['idPossibleReplies'],
            'idReply': id_reply,
            'success': success,
            'timeDisplay': "2019-01-21 00:02:21.029309",
            'timeReply': "2019-01-21 00:02:22.159123",
        }

        time.sleep(1)
        print(f"I'm sending {to_send}")
        print('\n')
        self.send(json.dumps(to_send))

    @classmethod
    def on_error(cls, error):
        if str(error) not in ['0', '']:
            print(f"I got error: {error}")

    @classmethod
    def on_close(cls):
        print("I'm closing")

    def on_open(self):

        to_send = {
            'userId': -1,
            'nIteration': self.n_iteration,
            'registerReplies': True,
            'teacher': 'leitner',
            't': -1,
            'idReply': -1,
            'timeDisplay': "<empty>",
            'timeReply': "<empty>",
        }

        print(f"I'm sending {to_send}")
        self.send(json.dumps(to_send))

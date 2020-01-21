# import requests
import json
import numpy as np

import time
from datetime import datetime

import websocket


class ActiveTeachingSocket(websocket.WebSocketApp):

    def __init__(self, url="ws://localhost:8000/",
                 waiting_time=1,
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
        self.waiting_time = waiting_time

    def decide(self, id_possible_replies, id_question, id_correct_answer):

        return np.random.choice(id_possible_replies)

    def on_message(self, json_string):

        print(f"I received: {json_string}")
        message = json.loads(json_string)

        if message['subject'] == 'sign_up':
            if message['ok'] is True:
                self.login()
            else:
                print('I encountered error for sign up...')
                self.close()

        elif message['subject'] == 'login':
            if message['ok'] is True:
                message = self.reply_to_question()
                self.send_dic_message(message)

            else:
                print("I will try to sign up")
                to_send = {
                    "subject": "sign_up",
                    "email": "nioche.aurelien@gmail.com",
                    "password": "1234",
                    "gender": "male",
                    "mother_tongue": "french",
                    "other_language": "english"
                }

                self.send(json.dumps(to_send))
                return

        else:
            message = self.reply_to_question()
            self.send_dic_message(message)

    @classmethod
    def on_error(cls, error):
        if str(error) not in ['0', '']:
            print(f"I got error: {error}")

    @classmethod
    def on_close(cls):
        print("I'm closing")

    def on_open(self):

        print("I'm open")
        self.login()

    def login(self):

        self.send_dic_message({
            "subject": "login",
            "email": "nioche.aurelien@gmail.com",
            "password": "1234",
        })

    def send_dic_message(self, message):

        print(f"I'm sending {message}")
        self.send(json.dumps(message))

    def reply_to_question(self, message):

        if message['t'] == -1:
            print("Done!")
            exit(0)

        id_possible_replies = message['id_possible_replies']
        id_correct_answer = message['id_correct_answer']
        id_question = message['id_question']

        # Timestamp for display
        # something like "2019-01-21 00:02:21.029309"
        message['time_display'] = \
            datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        id_reply = int(self.decide(
            id_possible_replies=id_possible_replies,
            id_question=id_question,
            id_correct_answer=id_correct_answer,
        ))

        # Small pause
        time.sleep(self.waiting_time)

        success = id_reply == id_correct_answer
        print("I got question", message["id_question"])
        print("I replied", id_reply)
        print(f"It was{' not ' if not success else ' '}a success")

        message['subject'] = 'reply'
        message['id_reply'] = id_reply

        message['time_reply'] = \
            datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        message['success'] = success
        return message

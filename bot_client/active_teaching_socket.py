# import requests
import json
import numpy as np

import time
from datetime import datetime

import websocket


from core.reception_desk import Request


class ActiveTeachingSocket(websocket.WebSocketApp):

    def __init__(self, url="ws://localhost:8000/",
                 email="nioche.aurelien@gmail.com",
                 password='1234',
                 gender='male',
                 mother_tongue='french',
                 other_language='english',
                 waiting_time=1,
                 **kwargs):
        super().__init__(
            url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open,
            **kwargs)

        self.email = email
        self.password = password
        self.waiting_time = waiting_time
        self.gender = gender
        self.mother_tongue = mother_tongue
        self.other_language = other_language

    def decide(self, id_possible_replies, id_question, id_correct_reply):

        return np.random.choice(id_possible_replies)

    def on_message(self, json_string):

        print(f"I received: {json_string}")
        message = Request(**json.loads(json_string))

        if message.subject == Request.SIGN_UP:
            if message.ok is True:
                self.login()
            else:
                print('I encountered error for sign up...')
                self.close()

        elif message.subject == Request.LOGIN:
            if message.ok is True:
                self.reply_to_question(message)
                return

            else:
                print("I will try to sign up")
                self.signup()
                return

        else:
            self.reply_to_question(message)
            return

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

    def send_message(self, message):
        
        string_msg = json.dumps(message.to_json_serializable_dic())
        print(f"I'm sending {string_msg}")
        self.send(string_msg)

    def login(self):

        message = Request(
            subject=Request.LOGIN,
            email=self.email,
            password=self.password)
        self.send_message(message)

    def signup(self):

        message = Request(
            subject=Request.SIGN_UP,
            email=self.email,
            password=self.password,
            gender=self.gender,
            mother_tongue=self.mother_tongue,
            other_language=self.other_language
        )
        self.send_message(message)

    def reply_to_question(self, message):

        if message.t == -1:
            print("Received t = -1 which is the Done!")
            exit(0)

        # Timestamp for display
        # something like "2019-01-21 00:02:21.029309"
        message.time_display = \
            datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        id_user_reply = int(self.decide(
            id_possible_replies=message.id_possible_replies,
            id_question=message.id_question,
            id_correct_reply=message.id_correct_reply,
        ))

        # Small pause
        time.sleep(self.waiting_time)

        success = id_user_reply == message.id_correct_reply
        print("I got question ID ", message.id_question)
        print("I replied ID ", id_user_reply)
        print(f"It was{' not ' if not success else ' '}a success")

        message.subject = Request.QUESTION
        message.id_user_reply = id_user_reply

        message.time_reply = \
            datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        message.success = success

        self.send_message(message)

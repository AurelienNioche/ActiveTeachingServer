# import requests
import json
import numpy as np

import time
from datetime import datetime

import websocket


from reception_desk.reception_desk import Subject


class RandomSocket(websocket.WebSocketApp):

    def __init__(self, url="ws://localhost:8001/",
                 email="leitner@test.com",
                 password='1234',
                 gender='male',
                 mother_tongue='french',
                 other_language='english',
                 waiting_time=1):

        super().__init__(
            url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open)

        self.email = email
        self.password = password
        self.waiting_time = waiting_time
        self.gender = gender
        self.mother_tongue = mother_tongue
        self.other_language = other_language

        self.user_id = None

    def decide(self, id_possible_replies, id_question, id_correct_reply,
               time_display, time_reply):

        return np.random.choice(id_possible_replies)

    def on_message(self, json_string):

        print(f"I received: {json_string}")
        message = json.loads(json_string)

        # if message.subject == Request.SIGN_UP:
        #     if message.ok is True:
        #         self.login()
        #     else:
        #         print('I encountered error for sign up...')
        #         self.close()

        if message["subject"] == Subject.LOGIN:
            if message["ok"]:
                self.user_id = message["user_id"]
                self.ask_for_session()
                return
            else:
                raise Exception("Can't login!")

            # else:
            #     print("I will try to sign up")
            #     self.signup()
            #     return

        elif message["subject"] == Subject.SESSION:
            self.join_session(message)
            return

        elif message["subject"] == Subject.QUESTION:
            self.reply_to_question(message)
            return

        else:
            raise ValueError

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
        
        string_msg = json.dumps(message)
        print(f"I'm sending {string_msg}")
        self.send(string_msg)

    def login(self):

        message = {
            "subject": Subject.LOGIN,
            "email": self.email,
            "password": self.password}
        self.send_message(message)

    def ask_for_session(self):

        message = {
            "subject": Subject.SESSION,
            "user_id": self.user_id,
        }
        self.send_message(message)

    def join_session(self, message):

        if message["available"]:
            message = {
                "subject": Subject.QUESTION,
                "user_id": self.user_id,
                "question_id": -1
            }
            self.send_message(message)
        elif "end" in message:
            print("This is this end")
        else:
            print(f"New available time: {message['available_time']}")
            # Small pause
            time.sleep(self.waiting_time)

            self.join_session(message)

    def reply_to_question(self, message):

        if "session_done" in message and message["session_done"]:
            print("End of the session")
            self.ask_for_session()
        else:

            id_q = message["question_id"]
            id_pr = message["id_possible_replies"]
            id_cr = message["id_correct_reply"]

            # Timestamp for display
            # something like "2019-01-21 00:02:21.029309"
            time_display = datetime.now()

            # Small pause
            time.sleep(self.waiting_time)

            time_reply = datetime.now()

            id_user_reply = int(self.decide(
                id_possible_replies=id_pr,
                id_question=id_q,
                id_correct_reply=id_cr,
                time_display=time_display,
                time_reply=time_reply
            ))

            success = id_user_reply == id_cr
            print("I got kanji ID ", id_q)
            print("I replied ID ", id_user_reply)
            print(f"It was{' not ' if not success else ' '}a success")

            message = {
                "subject": Subject.QUESTION,
                "user_id": self.user_id,
                "question_id": id_q,
                "id_user_reply": id_user_reply,
                "success": success,
                "time_display": time_display.strftime('%Y-%m-%d %H:%M:%S.%f'),
                "time_reply": time_reply.strftime('%Y-%m-%d %H:%M:%S.%f')
            }

            self.send_message(message)

    # def signup(self):
    #
    #     message = Request(
    #         subject=Request.SIGN_UP,
    #         email=self.email,
    #         password=self.password,
    #         gender=self.gender,
    #         mother_tongue=self.mother_tongue,
    #         other_language=self.other_language
    #     )
    #     self.send_message(message)
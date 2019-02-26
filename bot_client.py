# import requests
import time
import threading
import numpy as np
import multiprocessing as ml
import argparse
import json

import websocket
websocket.enableTrace(False)


# --------------- Init ----------------- #

class KeyInit:
    demand = "demand"
    device_id = "deviceId"

# -------------- Survey ----------------- #


class KeySurvey:
    demand = "demand"
    user_id = "userId"
    age = "age"
    sex = "sex"


# -------------- Play -------------------- #


class KeyChoice:
    demand = "demand"
    desired_good = "good"
    t = "t"
    user_id = "userId"

# ----------------------------------------- #


class BotClient:

    def __init__(self, url, device_id=0):

        self.ws = None
        self._connect(url)

        self.url = url

        self.device_id = device_id

        self.t = None
        self.state = None

        self.game_state = None

        self.training_end = None
        self.game_end = None

        self.wait_for_server = None

        self.last_request = None

        self.done_training_choice = None
        self.done_choice = None

        self.order = [
            self.init,
            self.end
        ]

    def _connect(self, url):

        # del self.ws

        print("Connect...")

        self.ws = websocket.WebSocketApp(
            url=url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        self.ws.on_open = self.on_open

        thread = threading.Thread(target=self.ws.run_forever)
        thread.daemon = True
        thread.start()

    def _request(self, data):

        print("sending ", data)
        self.ws.send(json.dumps(data))

    def on_open(self, *args):

        print('Connection established')

    def on_error(self, message, *args):

        print(message)
        # self._connect(url=self.url)
        # try:
        #     getattr(self, self.last_request)()
        # except:
        #     print('tamere')

    def on_close(self, message):

        print("websocket is closed.")
        # self._connect(url=self.url)

    def on_message(self, ws, args):

        data = json.loads(args)

        if isinstance(data, dict):

            print('Received:', data)

            if not data['wait']:
                self.last_request = data['demand']

                func = getattr(self, 'reply_' + data['demand'])

                func(data)

            else:
                print(f'Waiting, progress={data["progress"]}')

        else:
            print("Received:, ", data)
            print(data)

    # --------------------- Init ------------------------------------ #

    def init(self):

        self._request({
            KeyInit.demand: "init",
            KeyInit.device_id: self.device_id,
        })

    def reply_init(self, args):

        print(f"Received reply: {args}")

    def end(self):

        print('this is the end')


def main():

    url = "ws://127.0.0.1:8000/ws/chat/tamere/"
    # url = 'ws://money.getz.fr/ws/'

    bot = BotClient(url=url)
    bot.init()


if __name__ == "__main__":

    main()

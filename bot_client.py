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

# -------------- tuto ----------------- #


class KeyTuto:
    demand = "demand"
    user_id = "userId"
    progress = "progress"
    desired_good = "good"
    t = "t"


class KeyTutoDone:

    demand = "demand"
    user_id = "userId"
# -------------- Play -------------------- #


class KeyChoice:
    demand = "demand"
    desired_good = "good"
    t = "t"
    user_id = "userId"

# ----------------------------------------- #


class BotClient:

    def __init__(self, url, device_id):

        self.ws = None
        self._connect(url)

        self.url = url

        self.device_id = device_id

        self.t = None
        self.state = None
        self.user_id = None
        self.good_in_hand = None
        self.desired_good = None
        self.made_choice = None
        self.wait = None
        self.training_good = None
        self.training_t = None
        self.training_desired_good = None
        self.training_good_in_hand = None
        self.training_t_max = None
        self.t_max = None
        self.choice_made = None
        self.n_good = None

        self.game_state = None

        self.training_end = None
        self.game_end = None

        self.wait_for_server = None

        self.last_request = None

        self.done_init = False
        self.done_survey = False
        self.done_training = False

        self.done_training_choice = None
        self.done_choice = None

        self.mapping = {
                "survey": self.survey,
                "training": self.training_choice,
                "game": self.choice,
                "end": self.end
        }

        self.order = [
            self.init,
            self.survey,
            self.training_choice,
            self.training_done,
            self.choice,
            self.end
        ]

    def _connect(self, url):

        # del self.ws

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
        self._connect(url=self.url)
        # try:
        #     getattr(self, self.last_request)()
        # except:
        #     print('tamere')

    def on_message(self, ws, args):

        data = json.loads(args)

        if isinstance(data, dict):

            print('Received:', data)

            if not data['wait']:
                self.last_request = data['demand']

                func = getattr(self, 'reply_' + data['demand'])

                if data.get('receipt'):

                    self.user_id = data['userId'] if self.user_id is None else self.user_id

                    self.receipt_confirmation(
                        t=data.get('t'),
                        concerned_demand=data['demand']
                    )

                func(data)

            else:
                print(f'Waiting, progress={data["progress"]}')

        else:
            print("Received:, ", data)
            print(data)

    def get_desired_good(self, training=False):

        desired_good = np.random.randint(self.n_good)

        if training:
            while desired_good == self.training_good_in_hand:
                desired_good = np.random.randint(self.n_good)
        else:
            while desired_good == self.good_in_hand:
                desired_good = np.random.randint(self.n_good)

        return desired_good

    # ------------------------------------------------------------- #

    def receipt_confirmation(self, t, concerned_demand):

        self._request({
            "demand": "receipt_confirmation",
            "concernedDemand": concerned_demand,
            "t": t,
            "userId": self.user_id
        })

    # --------------------- Init ------------------------------------ #

    def init(self):

        self._request({
            KeyInit.demand: "init",
            KeyInit.device_id: self.device_id,
        })

    def reply_init(self, args):

        if not self.done_init:
            self.user_id = args["userId"]

            self.good_in_hand = args["goodInHand"]
            self.training_good_in_hand = args["trainingGoodInHand"]

            self.n_good = args["nGood"]

            if args["goodDesired"] != -2:
                self.desired_good = args["goodDesired"]

            else:
                self.desired_good = self.get_desired_good()

            if args["trainingGoodDesired"] != -2:
                self.training_desired_good = args["trainingGoodDesired"]

            else:
                self.training_desired_good = self.get_desired_good(training=True)

            self.t = args["t"] if args['t'] is not None else 0

            self.t_max = args["tMax"]
            self.choice_made = args["choiceMade"]
            self.training_t = args["trainingT"] if args['trainingT'] is not None else 0
            self.training_t_max = args["trainingTMax"]

            self.done_training_choice = np.zeros(self.training_t_max)
            self.done_choice = np.zeros(self.t_max)

            if not args['wait']:

                input(f'Go to state {args["step"]}?')

                self.done_init = True

                self.mapping[args['step']]()

    def survey(self):

        self._request({
            KeySurvey.demand: "survey",
            KeySurvey.age: 31,
            KeySurvey.sex: "female",
            KeySurvey.user_id: self.user_id,
        })

    def reply_survey(self, args):

        if not self.done_survey:

            if not args['wait']:
                self.done_survey = True

                input('Go to state training?')
                self.training_choice()

    # --------------------- tuto  ------------------------------------ #

    def training_choice(self):

        self._request({
            KeyTuto.demand: "training_choice",
            KeyTuto.progress: 100,
            KeyTuto.user_id: self.user_id,
            KeyTuto.desired_good: self.training_desired_good,
            KeyTuto.t: self.training_t,
        })

    def reply_training_choice(self, args):

        if not self.done_training_choice[args["t"]]:

            if not args["wait"]:

                self.done_training_choice[args["t"]] = 1

                if args["trainingSuccess"] != -2:

                    if args["trainingSuccess"]:

                        if self.training_desired_good == 1:
                            self.training_good_in_hand = 0
                        else:
                            self.training_good_in_hand = self.training_desired_good

                    self.training_desired_good = self.get_desired_good(training=True)

                    if args['trainingEnd']:
                        input('Go to state "training_done"?')
                        self.training_done()
                    else:
                        self.training_t = args["t"] + 1
                        self.training_choice()

                else:
                    raise Exception("Do not wait but success is None")

    def training_done(self):

        self._request({
            KeyTutoDone.demand: "training_done",
            KeyTutoDone.user_id: self.user_id
        })

    def reply_training_done(self, args):

        if not self.done_training:
            if not args['wait']:
                input('Go to state game?')
                self.done_training = True
                self.choice()

    # --------------------- choice ------------------------------------ #

    def choice(self):

        self._request({
            KeyChoice.demand: "choice",
            KeyChoice.user_id: self.user_id,
            KeyChoice.desired_good: self.desired_good,
            KeyChoice.t: self.t
        })

    def reply_choice(self, args):

        if not self.done_choice[args['t']]:

            if not args["wait"]:

                self.done_choice[args['t']] = 1

                if args["success"] != -2:

                    if args["success"]:

                        if self.desired_good == 1:
                            self.good_in_hand = 0
                        else:
                            self.good_in_hand = self.desired_good

                    self.desired_good = self.get_desired_good()

                    if args['end']:
                        self.end()
                    else:
                        self.t = args['t'] + 1
                        self.choice()

                else:
                    raise Exception("Do not wait but success is None")

    def end(self):
        print('this is the end')


def bot_factory(base, device_id, delay, url, wait_event, seed):

    class BotProcess(base):

        def __init__(self):

            super().__init__()

            self.b = BotClient(url=url, device_id=device_id)
            self.delay = delay
            self.ml = isinstance(self, threading.Thread)
            self.wait_event = wait_event

        def wait(self):

            self.wait_event(self.delay)

        def run(self):

            np.random.seed(seed)

            if not self.ml:
                input("Run? Press a key.")

            self.b.init()

            while True:
                self.wait()

    return BotProcess()


def main(args):

    url = "ws://127.0.0.1/ws/register"
    # url = 'ws://money.getz.fr/ws/'

    if not args.number:

        n = input("Bot id? > ")
        device_id = "bot{}".format(n)

        b = bot_factory(
            base=object,
            wait_event=time.sleep,
            url=url,
            device_id=device_id,
            delay=2,
            seed=1
        )

        b.run()

    else:

        n = int(args.number)

        for b in range(n):

            device_id = "bot{}".format(b)

            bot = bot_factory(
                base=threading.Thread,
                wait_event=ml.Event().wait,
                url=url,
                device_id=device_id,
                delay=1,
                seed=b,
            )

            bot.start()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Run bots.')

    parser.add_argument('-n', '--number', action="store", default=None,
                        help="number of bots")

    parsed_args = parser.parse_args()

    main(parsed_args)



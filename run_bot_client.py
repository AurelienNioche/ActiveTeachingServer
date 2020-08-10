import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import websocket

from bot_client.random_socket import RandomSocket
from bot_client.learner_socket import LearnerSocket
from bot_client.learning_model.exponential_forgetting import ExponentialNDelta
# from bot_client.learning_model.act_r.act_r import ActR


def run_random():

    ws = RandomSocket()
    ws.run_forever()


def run_exp_decay():

    websocket.enableTrace(True)
    ws = LearnerSocket(
        cognitive_model=ExponentialNDelta,
        waiting_time=1,
        param=[0.02, 0.44])
    ws.run_forever()


def main():

    websocket.enableTrace(True)
    run_random()


if __name__ == "__main__":

    run_exp_decay()

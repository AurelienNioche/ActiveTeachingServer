import websocket

from bot_client.basic import MySocket
from bot_client.learner import LearnerSocket
from bot_client.learning_model.act_r.act_r import ActR
from bot_client.learning_model.hopfield_network.carlos_hopfield import Hopfield

websocket.enableTrace(True)


def run_random():

    ws = MySocket(register_replies=False)
    ws.run_forever()


def run_act_r():

    ws = LearnerSocket(
        cognitive_model=ActR,
        waiting_time=0,
        n_iteration=1000,
        param={"d": 0.5, "tau": 0.01, "s": 0.06})
    ws.run_forever()


def run_hopfield():

    ws = LearnerSocket(
        cognitive_model=Hopfield,
        waiting_time=0,
        n_iteration=1000,
        param={"learning_rate": 0.0001, "forgetting_rate": 0.000001})
    ws.run_forever()


def main():

    run_hopfield()


if __name__ == "__main__":

    main()

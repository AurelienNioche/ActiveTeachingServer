import websocket

from bot_client.basic import ActiveTeachingSocket
from bot_client.learner import LearnerSocket
from bot_client.learning_model.act_r.act_r import ActR


def run_random():

    ws = ActiveTeachingSocket(register_replies=True)
    ws.run_forever()


def run_act_r():

    ws = LearnerSocket(
        cognitive_model=ActR,
        waiting_time=0,
        n_iteration=1000,
        param={"d": 0.5, "tau": 0.01, "s": 0.06})
    ws.run_forever()


def main():

    websocket.enableTrace(True)
    run_random()


if __name__ == "__main__":

    main()

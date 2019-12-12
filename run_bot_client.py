# import websocket

from bot_client.basic import MySocket
from bot_client.learner import LearnerSocket
from bot_client.learning_model.rl import QLearner

# TEACHING_MATERIAL = "kanji"
# TEACHING_MATERIAL = "finnish"
TEACHING_MATERIAL = "japanese"


def run_random():
    ws = MySocket(register_replies=False, teaching_material=TEACHING_MATERIAL)
    ws.run_forever()


def run_rl():

    ws = LearnerSocket(cognitive_model=QLearner)
    ws.run_forever()


def main():
    # websocket.enableTrace(True)
    run_random()
<<<<<<< HEAD

=======
    # run_act_r()
>>>>>>> fixes

if __name__ == "__main__":
    main()

import websocket

from bot_client.basic import MySocket
from bot_client.learner import LearnerSocket
from bot_client.learning_model.act_r.act_r import ActR

# TEACHING_MATERIAL = "kanji"
# TEACHING_MATERIAL = "finnish"
TEACHING_MATERIAL = "japanese" #"kanji"# "finnish" # "kanji

def run_random():
    ws = MySocket(register_replies=False, teaching_material=TEACHING_MATERIAL)
    ws.run_forever()


def run_act_r():
    ws = LearnerSocket(
        cognitive_model=ActR,
        waiting_time=0,
        n_iteration=1000,
        teaching_material=TEACHING_MATERIAL,
        param={"d": 0.5, "tau": 0.01, "s": 0.06})
    ws.run_forever()



def main():
    websocket.enableTrace(True)
    # run_random()
    run_act_r()

if __name__ == "__main__":
    main()

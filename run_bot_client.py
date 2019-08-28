import websocket

from bot_client.basic import MySocket


def run_random():

    websocket.enableTrace(True)
    ws = MySocket("ws://localhost:8000/")
    ws.run_forever()


def run_act_r():

    pass


def main():

    run_random()


if __name__ == "__main__":

    main()

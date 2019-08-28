# import requests
import json
import numpy as np

import time

import websocket
websocket.enableTrace(False)


def on_message(ws, message):

    print(f"I received: {message}")
    message = json.loads(message)

    if message['t'] == -1:
        exit(0)

    id_reply = int(np.random.choice(message['idPossibleReplies']))
    success = id_reply == message['idCorrectAnswer']
    print("I got question", message["idQuestion"])
    print("I replied", id_reply)
    print(f"It was{' not ' if not success else ' '}a success")

    to_send = {
        'userId': message['userId'],
        'nIteration': message['nIteration'],
        'registerReplies': message['registerReplies'],
        'teacher': 'leitner',
        't': message['t'],
        'idQuestion': message["idQuestion"],
        'idCorrectAnswer': message['idCorrectAnswer'],
        'idPossibleReplies': message['idPossibleReplies'],
        'idReply': id_reply,
        'success': success,
        'timeDisplay': "2019-01-21 00:02:21.029309",
        'timeReply': "2019-01-21 00:02:22.159123",
    }

    time.sleep(1)
    print(f"I'm sending {to_send}")
    print('\n')
    ws.send(json.dumps(to_send))

    # thread.start_new_thread(run, ())


def on_error(ws, error):
    if str(error) != '0':
        print(f"I got error: {error}")


def on_close(ws):
    print("I'm closing")


def on_open(ws):

    to_send = {
        'userId': -1,
        'nIteration': 10,
        'registerReplies': True,
        'teacher': 'leitner',
        't': -1,
        'idReply': -1,
        'timeDisplay': "<empty>",
        'timeReply': "<empty>",
    }

    print(f"I'm sending {to_send}")
    ws.send(json.dumps(to_send))


def main():

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "ws://localhost:8000/",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    ws.run_forever()


if __name__ == "__main__":

    main()

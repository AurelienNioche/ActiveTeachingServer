# import requests
import json

try:
    import thread
except ImportError:
    import _thread as thread
import time

import websocket
websocket.enableTrace(False)


def on_message(ws, message):

    def run(*args):
        while True:

            if message['t'] != -1:

                to_send = {
                    'userId': message['userId'],
                    't': message['t'] + 1,
                    'reply': "Bouh",
                    'timeDisplay': "2019-01-21 00:02:21.029309",
                    'timeReply': "2019-01-21 00:02:22.159123",
                }

                time.sleep(1)
                print(f"I'm sending {to_send}")
                ws.send(json.dumps(to_send))

            else:
                break

    print(f"I received: {message}")

    thread.start_new_thread(run, ())


def on_error(ws, error):
    print(f"I got error: {error}")


def on_close(ws):
    print("I'm closing")


def on_open(ws):

    to_send = {
        'userId': -1,
        't': -1,
        'reply': "<empty>",
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

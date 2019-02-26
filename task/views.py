from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the task index.")


@csrf_exempt
def client_request(request):

    """
    main method taking request from client
    and returning
    :param request:
    :return: response
    """

    # Log
    print("Websocket request: {}".format(list(request.items())))

    demand = request.get('demand')

    if not demand:
        raise Exception('"demand" key is required.')

    # Retrieve functions in current script
    functions = {
        f_name: f for f_name, f in globals().items()
        if not f_name.startswith("_")
    }

    # Retrieve demanded function from current script
    func = functions.get(demand)

    if not func:
        raise Exception("Bad demand.")

    to_reply = {'response': 'hey'}

    return to_reply


def connect(name):

    print(f"Name of the client is: {name}")

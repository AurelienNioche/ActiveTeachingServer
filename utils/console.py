import sys


class AskUser:

    def __init__(self, f):
        self.f = f

    def __call__(self, **kwargs):

        while True:
            r = input("Are you sure you want to operate this change?")
            r.lower()
            if r == 'n':
                sys.exit()
            elif r == 'y':
                break
            else:
                print("Your response have to be 'y' or 'n'!")
        self.f(**kwargs)
        print("Done!")
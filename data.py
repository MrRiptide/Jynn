import os


def get_token():
    if os.path.isfile("token"):
        token_file = open("token", "r")
        token = token_file.readline()
        return token
    else:
        raise FileNotFoundError('Missing a token file, should be named "token" and in the same folder as "main.py"')

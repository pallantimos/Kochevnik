import os
import random
import string

from dotenv import dotenv_values

config = dotenv_values(".env")


class Config(object):
    SECRET_KEY = 'ddcfeef4ea497be79f25fcac5c4afdc6d83cb88a'


def random_string():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))



from huey import SqliteHuey

huey = SqliteHuey(filename='demo.db')

@huey.task()
def add(a, b):
    return a + b

import time

@huey.task()
def long():
    time.sleep(10)
    return 10

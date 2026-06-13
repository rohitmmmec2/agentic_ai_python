from Radis import Radis
from rq import Queue

queue = Queue(connection=Radis(
host='localhost',
port=6379,
))

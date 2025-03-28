from pymongo import MongoClient
from os import getenv
client = MongoClient(getenv("MONGO_URI"))
db = client["GanepLar"]

__all__ = [
    'MongoClient',
    'client',
    'db'
]
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["GanepLar"]


__all__ = [
    'MongoClient',
    'client',
    'db'
]
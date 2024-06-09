import os

from pymongo import MongoClient


def get_mongo_collection(database, collection):
    # e.g. MONGODB_URI=mongodb://mongo:mongo@127.0.0.1:27017/
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client[database]
    return db[collection]

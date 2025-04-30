from db_connect import main as db_connector
from datetime import datetime

db = db_connector()

feeds_collection = db[1].feeds

for doc in feeds_collection.find():
    feeds_collection.update_one(
        {"_id": doc["_id"]},
        {"$set": {"language": "eng"}}
    )
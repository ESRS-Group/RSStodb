from testdb_connect import main as db_connector
from datetime import datetime

db = db_connector()

articles_collection = db[1].articles


for doc in articles_collection.find():
    if isinstance(doc.get("published"), str):
        try:
            date = datetime.strptime(doc["published"], "%a, %d %b %Y %H:%M:%S %Z")
            articles_collection.update_one({"_id": doc["_id"]}, {"$set": {"published": date}})
            print(f"Updated {date}")
        except ValueError as e:
            print(f"Skipping {doc['_id']} due to error: {e}")
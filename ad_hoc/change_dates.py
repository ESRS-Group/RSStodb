from db_connect import main as db_connector
from datetime import datetime

db = db_connector()

articles_collection = db[1].articles

result = articles_collection.update_many(
    {},
    {
        "$set": {
            "o_language": "en",
            "translated": False
        },
        "$unset": {
            "o": ""  # This removes the entire "o" field
        }
    }
)

print(f"Modified {result.modified_count} documents.")

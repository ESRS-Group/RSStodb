from db_connect import main as connect_to_db
from bson.objectid import ObjectId
from collections import defaultdict


DUPLICATE_FIELDS = ['title'] 
COLLECTION_NAME = 'articles' 

def remove_duplicates():
    success, db = connect_to_db()
    if not success:
        print("Failed to connect to database.")
        return

    collection = db[COLLECTION_NAME]

    
    seen = defaultdict(list)

    for doc in collection.find():
        key = tuple(doc.get(field) for field in DUPLICATE_FIELDS)
        print(key)
        seen[key].append(doc['_id'])

    
    for key, ids in seen.items():
        if len(ids) > 1:
            
            print(f"Duplicate found for key {key}:")
            duplicates = collection.find({'_id': {'$in': ids}})
            for dup in duplicates:
                print(dup)

            to_delete = ids[1:] 
            result = collection.delete_many({'_id': {'$in': to_delete}})
            print(f"Deleted {result.deleted_count} duplicate(s) for key {key}\n")

    print("Duplicate removal complete.")



if __name__ == '__main__':
    remove_duplicates()
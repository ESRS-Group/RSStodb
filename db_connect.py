from pymongo import MongoClient , errors
import certifi



def main():
    try:
        client = MongoClient("mongodb+srv://ringofthelords:frodo123@esrsdb.awdlh.mongodb.net/", tlsCAFile=certifi.where())
        db = client.esrsdb
        return (True, db)
    except errors.ServerSelectionTimeoutError as err:
        return (False, err)

if __name__ == "__main__":
    main()
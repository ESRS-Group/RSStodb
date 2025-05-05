from pymongo import MongoClient , errors
import certifi

def main():
    try:
        client = MongoClient("mongodb+srv://<user_name>:<password>@esrsdb.awdlh.mongodb.net/esrsdb", tlsCAFile=certifi.where())
        db = client.esrsdb
        return(True, db)
    except errors.ServerSelectionTimeoutError as err:
        return(False, err)

if __name__ == "__main__":
    main()
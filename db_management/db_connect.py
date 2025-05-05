from pymongo import MongoClient , errors
import certifi

def main():
    try:
        client = MongoClient("mongodb+srv://back_end:wr0cC5VPlrbfoFKL@esrsdb.awdlh.mongodb.net/esrsdb", tlsCAFile=certifi.where())
        db = client.esrsdb
        return(True, db)
    except errors.ServerSelectionTimeoutError as err:
        return(False, err)

if __name__ == "__main__":
    main()
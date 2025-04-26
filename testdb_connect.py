from pymongo import MongoClient , errors
import certifi

def main():
    try:
        client = MongoClient("mongodb+srv://ringlord:freddo3@esrstest.yf1qd.mongodb.net/esrs_test" , tlsCAFile=certifi.where())
        db = client.esrs_test
        return (True, db)
    except errors.ServerSelectionTimeoutError as err:
        return (False, err)

if __name__ == "__main__":
    main()
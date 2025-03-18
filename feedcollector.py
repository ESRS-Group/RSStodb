from pymongo import errors
from rss_parser import rss_parser
from db_connect import main as db_connector
import requests
from datetime import datetime

def main():

    db = db_connector()
    

    if db[0]:
        articles_collection = db[1].articles
        feeds_collection = db[1].feeds
        articles_collection.create_index("link", unique=True)
    else:
        return db[1] 

    url = input()
    provider = input()
    genre = input()

    articles = rss_parser([provider, genre, url])
    articles_present = articles[0]
    articles_list = articles[1]

    if articles_present:

        errors_list = []
        feeds_collection.update_one({"url": url}, {"$set": { "Last_Update": datetime.now()}})

        for article in articles_list:
            try:
                articles_collection.insert_one(article)
                print(True, None)                
            except Exception as err:
                errors_list.append((article["link"], err))
        print(True, errors_list)
    
    else:
        print(False, "No articles found")

if __name__ == "__main__":
    main()
        



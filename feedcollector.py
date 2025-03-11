from pymongo import MongoClient , errors
import feedparser
import certifi
import requests
from datetime import datetime


def rss_parser(feed : list) -> tuple[bool, list]:
    provider : str = feed[0]
    genre : str = feed[1]
    feed_url = feed[2]

    try:
        response = requests.get(feed_url)

        if response.status_code == 200:
            feed_data = feedparser.parse(response.text)
            entries = feed_data.entries
        else:
            print(f"Failed to fetch the feed: {response.status_code}")
            return False, response.status_code
        
    except requests.exceptions.RequestException as err:
        return False, err

    articles = []    

    for entry in entries:
        articles.append({
            "provider": provider,
            "genre": genre,
            "title": entry.title,
            "link":entry.link,
            "summary": entry.get("summary", ""),
            "published": entry.get("published", ""),
            "source": feed_data.feed.get("title", "Unknown Source")
        })
    
    return True, articles

def main():

    try:
        client = MongoClient("mongodb+srv://ringofthelords:frodo123@esrsdb.awdlh.mongodb.net/", tlsCAFile=certifi.where())
        db = client.esrsdb
        articles_collection = db.articles
        feeds_collection = db.feeds
        articles_collection.create_index("link", unique=True)
    except errors.ServerSelectionTimeoutError as err:
        return err 

    url = input()
    provider = input()
    genre = input()

    articles = rss_parser([provider, genre, url])

    if articles[0]:

        feeds_collection.update_one({"url": url}, {"$set": { "Last_Update": datetime.now()}})

        for article in articles[1]:
            try:
                articles_collection.insert_one(article)
                return True, None
            except errors.DuplicateKeyError as err:
                return False, err
            except Exception as err:
                return False, err
    
    else:
        print(articles[1])

if __name__ == "__main__":
    main()
        



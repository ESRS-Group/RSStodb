from pymongo import MongoClient , errors
import schedule
import time
from rss_parser import rss_parser


client = MongoClient("mongodb+srv://ringofthelords:frodo123@esrsdb.awdlh.mongodb.net/")
db = client.esrsdb

articles_collection = db.articles
feeds_collection = db.feeds
articles_collection.create_index("link", unique=True)

def save_articles(articles_list):
    for article in articles_list:
        try:
            articles_collection.insert_one(article)
        except errors.DuplicateKeyError:
            print(f"Duplicate record found {article["title"]} not added.")
        except Exception as e:
            print(f"Failed to save article '{article['title']}': {e}")


feeds_collection = db.feeds

feeds = feeds_collection.find({})
urls = []

for item in feeds:
    urls.append([item["provider"], item["genre"], item["url"]])

def fetch_and_save_feeds():
    for url in urls:
        articles = rss_parser(url)[1]
        save_articles(articles)


schedule.every(1).minutes.do(lambda: fetch_and_save_feeds())

while True:
    schedule.run_pending()
    time.sleep(1)
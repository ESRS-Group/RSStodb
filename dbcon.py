from pymongo import MongoClient , errors
import feedparser
import schedule
import time

client = MongoClient("mongodb+srv://ringofthelords:frodo123@esrsdb.awdlh.mongodb.net/")

db = client.esrsdb

articles_collection = db.articles
feeds_collection = db.feeds

articles_collection.create_index("link", unique=True)

def rss_parser(feed):
    provider = feed[0]
    genre = feed[1]
    url = feed[2]
    feed = feedparser.parse(url)
    articles_list = []

    if feed.entries == None:
        print(f"No articles found in url {url}")
        print(f"Raw data: {feed}")
        return []
    
    for entry in feed.entries:
        link = entry.link
        print(link)
        if ".com" in link:
            link = link.replace(".com", ".co.uk")   # short term fix for bbc issue which was pulling mostly .com addresses and we need .co.uk. Will fix properly ASAP

        articles_list.append({
            "provider": provider,
            "genre": genre,
            "title": entry.title,
            "link": link,
            "summary": entry.get("summary", ""),
            "published": entry.get("published", ""),
            "source": feed.feed.get("title", "Unknown Source")
        })
    
    print(f"Fetched {len(articles_list)} from {url}")
    return articles_list

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
        articles = rss_parser(url)
        save_articles(articles)


schedule.every(1).minutes.do(lambda: fetch_and_save_feeds())

while True:
    schedule.run_pending()
    time.sleep(1)
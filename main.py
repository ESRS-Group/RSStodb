import feedparser
import mysql.connector
import schedule
import time


def rss_parser(url):

    feed = feedparser.parse(url)
    articles_list = []

    if feed.entries == None:
        print(f"No articles found in url {url}")
        print(f"Raw data: {feed}")
        return []
    
    for entry in feed.entries:
        articles_list.append({
            "title": entry.title,
            "link": entry.link,
            "summary": entry.get("summary", ""),
            "published": entry.get("published", ""),
            "source": feed.feed.get("title", "Unkiwn Source")
        })
    
    print(f"Fetched {len(articles_list)} from {url}")
    return articles_list

def save_articles(articles_list):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="news_aggregator"
    )

    if conn.is_connected():
        print("Connected to MySQL database")
    else:
        print("Failed to connect to the database")

    cursor = conn.cursor()

    for article in articles_list:
        try:
            cursor.execute('''
                INSERT INTO articles (title, link, summary, published, source)
                VALUES (%s, %s, %s, %s, %s)
            ''', (article['title'], article['link'], article['summary'], article['published'], article['source']))
            print(f"Saved: {article['title']}")

        except mysql.connector.IntegrityError as e:
            print(f"Failed to save. {e}")
    
    conn.commit()
    conn.close()

links = [
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml"
]

def fetch_and_save_feeds():
    for url in links:
        articles = rss_parser(url)
        save_articles(articles)


schedule.every(1).minutes.do(lambda: fetch_and_save_feeds())

while True:
    schedule.run_pending()
    time.sleep(1)


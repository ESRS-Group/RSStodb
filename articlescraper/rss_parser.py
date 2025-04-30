import feedparser
import requests
from datetime import datetime

def rss_parser(feed : list) -> tuple[bool, list]:
    provider : str = feed[0]
    genre : str = feed[1]
    feed_url = feed[2]

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; RSSFetcher/1.0; +https://yourdomain.com/)"
    }

    try:
        response = requests.get(feed_url, headers=headers, timeout=10)

        if response.status_code == 200:
            feed_data = feedparser.parse(response.text)
            entries = feed_data.entries
        else:
            print(f"Failed to fetch the feed: {response.status_code}")
            return False, response.status_code
        
    except requests.exceptions.RequestException as e:
        return False, e

    articles = []    

    for entry in entries:
        published_str = entry.get("published", "").strip()
        if published_str:
            try:
                published_date = datetime.strptime(published_str, "%a, %d %b %Y %H:%M:%S %Z")
            except ValueError:
                published_date = datetime.now()
        else:
            published_date = datetime.now()
        articles.append({
            "provider": provider,
            "genre": genre,
            "title": entry.title,
            "link":entry.link,
            "summary": entry.get("summary", ""),
            "published": published_date,
            "source": feed_data.feed.get("title", "Unknown Source")
        })
    
    return True, articles


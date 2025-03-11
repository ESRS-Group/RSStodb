import feedparser
import requests
import pprint

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
        
    except requests.exceptions.RequestException as e:
        return False, e

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


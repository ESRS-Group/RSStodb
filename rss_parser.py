import feedparser

def rss_parser(feed : list) -> tuple[bool, list]:
    provider : str = feed[0]
    genre : str = feed[1]
    url : str = feed[2]

    feed_data = feedparser.parse(url)

    if feed_data.bozo == 1:
        return False, "RSS Feed Error"        # placeholder bool/str tuples returned in lieu of logging.

    if hasattr(feed_data, "status") and feed_data.status >= 400:
        return False, "HTTP error"

    if not feed_data.entries:
        return False, "No data found from RSS url"
    

    articles_list = []

    for entry in feed_data.entries:

        link = entry.link
        if ".com" in link:
            link = link.replace(".com", ".co.uk")   # short term fix for bbc issue which was pulling mostly .com addresses and we need .co.uk. Will fix properly ASAP

        articles_list.append({
            "provider": provider,
            "genre": genre,
            "title": entry.title,
            "link": link,
            "summary": entry.get("summary", ""),
            "published": entry.get("published", ""),
            "source": feed_data.feed.get("title", "Unknown Source")
        })
    
    return True, articles_list

from rss_parser import rss_parser
from db_connect import main as db_connector
from pymongo import errors
from datetime import datetime
from translation import main as translator

def lambda_handler(event, context):
    """
    Scheduled Lambda function to collect RSS articles hourly.
    - Connects to MongoDB using db_connect.py
    - Parses all feeds in mongodb feeds collection using rss_parser.py
    - Filters duplicate articles already found in articles collection via "provider" and "title".
    - Saves non-duplicates to articles collection.
    - Logs parsing stats to Cloudwatch (via print function)
    """

    db = db_connector()
    if not db[0]:
        print(f"Database connection failed: {db[1]}")
        return {
            "statusCode": 500,
            "body": "Database connection failed."
        }

    articles_collection = db[1].articles
    feeds_collection = db[1].feeds

    articles_collection.create_index("link", unique=True)

    feeds = feeds_collection.find()

    errors_list = []
    success_count = 0
    dup_count = 0
    fail_count = 0
    for feed in feeds:
        provider = feed.get("provider")
        genre = feed.get("genre")
        url = feed.get("url")
        language = feed.get("language")
        

        if not all([provider, genre, url]):
            print(f"Skipping incomplete feed config: {feed}")
            continue

        success, articles_list = rss_parser([provider, genre, url])    ## RSS scraper call.


        if success:
            feeds_collection.update_one(
                {"url": url},
                {"$set": {"Last_Update": datetime.now()}}
            )
            for article in articles_list:
                article["translated"] = False
                article["o_language"] = language

                existing = articles_collection.find_one({
                "title": article["title"],
                "provider": provider})

                if existing:
                    dup_count += 1
                    continue

                try:
                    articles_collection.insert_one(article)
                    success_count += 1
                except errors.DuplicateKeyError:
                    dup_count += 1
                    pass
                except Exception as err:
                    errors_list.append((article["link"], str(err)))
                    fail_count += 1
        else:
            errors_list.append((url, str(articles_list)))

    if errors_list:
        print({
            "statusCode": 207,
            "body": {"errors": errors_list}
        })
    else:
        print({
            "statusCode": 200,
            "body": "All feeds updated successfully."
        })
    
    print(f"Articles Saved:{success_count}") 
    print(f"Duplicate Articles:{dup_count}")
    print(f"Failed Articles:{fail_count}")
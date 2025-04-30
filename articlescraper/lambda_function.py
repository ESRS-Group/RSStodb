from rss_parser import rss_parser
from testdb_connect import main as db_connector
from pymongo import errors
from datetime import datetime

def lambda_handler(event, context):
    """
    Scheduled Lambda function to collect RSS articles hourly.
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

    for feed in feeds:
        provider = feed.get("provider")
        genre = feed.get("genre")
        url = feed.get("url")

        if not all([provider, genre, url]):
            print(f"Skipping incomplete feed config: {feed}")
            continue

        success, articles_list = rss_parser([provider, genre, url])

        if success:
            feeds_collection.update_one(
                {"url": url},
                {"$set": {"Last_Update": datetime.now()}}
            )
            for article in articles_list:
                try:
                    articles_collection.insert_one(article)
                except errors.DuplicateKeyError:
                    # It's okay, article already exists
                    pass
                except Exception as err:
                    errors_list.append((article["link"], str(err)))
        else:
            errors_list.append((url, str(articles_list)))

    if errors_list:
        return {
            "statusCode": 207,
            "body": {"errors": errors_list}
        }
    else:
        return {
            "statusCode": 200,
            "body": "All feeds updated successfully."
        }
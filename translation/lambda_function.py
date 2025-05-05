from db_connect import main as db_connector
from translation import main as translator
from datetime import datetime, timezone

def lambda_handler(event, context):
    """
    Scheduled Lambda function to collect RSS articles hourly.
    - Connects to MongoDB using db_connect.py
    - Filters articles collection for foreign articles not translated.
    - Translates using translation.py (sent to translation API)
    - Logs translation stats to Cloudwatch (via return response)
    """

    db = db_connector()
    if not db[0]:
        print(f"Database connection failed: {db[1]}")
        return {
            "statusCode": 500,
            "body": "Database connection failed."
        }

    articles_collection = db[1].articles

    to_be_translated = articles_collection.find({
        "o_language": {"$ne": "en"},
        "translated": False
    })

    translated_count = 0
    failed_translations = []

    for article in to_be_translated:
        lang = article.get("o_language")
        title = article.get("title", "")
        summary = article.get("summary", "")
        link = article.get("link")

        title_translation = translator(lang, title)
        summary_translation = translator(lang, summary)

        if title_translation[0] and summary_translation[0]:
            try:
                articles_collection.update_one(
                    {"_id": article["_id"]},
                    {
                        "$set": {
                            "title": title_translation[1],
                            "summary": summary_translation[1],
                            "translated": True,
                            "translated_at": datetime.now(timezone.utc)
                        }
                    }
                )
                translated_count += 1
            except Exception as e:
                failed_translations.append((link, str(e)))
        else:
            reason = f"Title: {title_translation[1]}, Summary: {summary_translation[1]}"
            failed_translations.append((link, reason))

    response = {
        "statusCode": 207 if failed_translations else 200,
        "body": {
            "translated_articles": translated_count,
            "failed_articles": len(failed_translations),
            "errors": failed_translations
        }
    }

    print(response)
    return response

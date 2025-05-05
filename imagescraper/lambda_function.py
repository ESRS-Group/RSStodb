from bs4 import BeautifulSoup
from db_connect import main as db_connector
import requests
import certifi
from pymongo import errors

def find_image(url, class_code):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ImageFetcher/1.0; +https://yourdomain.com/)"
    }
    try:
        r = requests.get(url=url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "html.parser")
        image_section = str(soup.find(class_=class_code))
        section = image_section.find("src=")
        return image_section[section:].split('"')[1]
    except Exception as e:
        print(f"Error fetching image from {url}: {e}")
        return None

def lambda_handler(event, context):
    print("Starting Lambda execution for missing images...")

    try:
        db = db_connector()
        if not db[0]:
            print(f"Database connection failed: {db[1]}")
            return {
                "statusCode": 500,
                "body": "Database connection failed."
            }
        db = db[1]
    except errors.PyMongoError as err:
        print(f"Database connection error: {err}")
        return {
            "statusCode": 500,
            "body": "MongoDB connection error."
        }

    articles_collection = db.articles
    configs_collection = db.configs

    missing_images = articles_collection.find({"image": None})
    missing_count = articles_collection.count_documents({"image": None})
    print(f"Found {missing_count} articles missing images.")

    updates = 0
    failures = []

    for item in missing_images:
        url = str(item.get("link", ""))
        provider = str(item.get("provider", ""))

        if not url or not provider:
            print("Skipping article with missing URL or provider.")
            continue

        config = configs_collection.find_one({"provider": provider})
        if not config:
            print(f"No config found for provider: {provider}")
            continue

        class_code = config.get("image_class")
        if not class_code:
            print(f"No image_class specified for provider: {provider}")
            continue

        image_url = find_image(url, class_code)

        if image_url:
            try:
                articles_collection.update_one(
                    {"link": url},
                    {"$set": {"image": image_url}}
                )
                updates += 1
                print(f"Updated image for article: {url}")
            except errors.PyMongoError as err:
                print(f"Error updating article {url}: {err}")
                failures.append((url, str(err)))
        else:
            print(f"Failed to find image for {url}")
            failures.append((url, "No image found"))

    print(f"Finished processing. Images updated: {updates}. Failures: {len(failures)}")

    return {
        "statusCode": 200,
        "body": {
            "updates": updates,
            "failures": failures
        }
    }

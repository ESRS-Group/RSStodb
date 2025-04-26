from bs4 import BeautifulSoup
from pymongo import MongoClient , errors
import requests
import certifi


def find_image(url, class_code):
        r = requests.get(url=url)
        soup = BeautifulSoup(r.content, "lxml")
        image_section = str(soup.find(class_=class_code))
        section = image_section.find("src=") 
        return image_section[section:].split('"')[1]

def main():
    try:
        client = MongoClient("mongodb+srv://ringofthelords:frodo123@esrsdb.awdlh.mongodb.net/", tlsCAFile=certifi.where())
        db = client.esrsdb
        articles_collection = db.articles
        configs_collection = db.configs
    except errors as err:
        return err
 
    missing_images = articles_collection.find({"image" : None})
    print(missing_images)
    for item in missing_images:
        url = str(item["link"])
        provider = str(item["provider"])
        config = configs_collection.find_one({"provider": provider})
        class_code = str(config["image_class"])
        try: 
            image = find_image(url, class_code)
            print(image)
            articles_collection.update_one({"link" : url}, {"$set": {"image" : image}})
            print("success")
        except errors.DuplicateKeyError as err:
            print(False, err)
        except Exception as err:
            print(False, err)


if __name__ == "__main__":
    main()
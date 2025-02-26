from bs4 import BeautifulSoup
from pymongo import MongoClient , errors
import requests


client = MongoClient("mongodb+srv://ringofthelords:frodo123@esrsdb.awdlh.mongodb.net/")

db = client.esrsdb

articles_collection = db.articles
configs_collection = db.configs

bbc = configs_collection.find_one({"provider": "BBC"})

class_image = str(bbc["image_class"])




def find_image(url, class_code):
    r = requests.get(url=url)
    soup = BeautifulSoup(r.content, "lxml")
    image_section = str(soup.find(class_=class_code))
    section = image_section.find("src=") 
    return image_section[section:].split('"')[1]

 
missing_images = articles_collection.find({"image" : None})

for item in missing_images:

    url = str(item["link"])
    print(url)
    provider = str(item["provider"])
 
    config = configs_collection.find_one({"provider": provider}) 
    class_code = str(config["image_class"])

    try: 
        image = find_image(url, class_code)
        articles_collection.update_one({"link" : url}, {"$set": {"image" : image}})
    except:
        continue

from bs4 import BeautifulSoup
import requests


urls = {"new statesman" : "https://www.newstatesman.com/international-politics/2025/02/germany-election-afd-far-right",
      "daily heil" : "https://www.dailymail.co.uk/tvshowbiz/article-14433415/eastenders-stars-enjoyed-secret-offscreen-romance-years.html",
      "CNN" : "https://edition.cnn.com/2025/02/25/uk/uk-defense-spending-increase-trump-intl/index.html",
      "BBC" : "https://www.bbc.co.uk/news/articles/cvgenz02lp8o",
      "aljaz" : "https://www.aljazeera.com/news/2025/2/25/ukrainian-parliament-affirms-zelenskyys-legitimacy",
      "South China News" : "https://www.scmp.com/news/hong-kong/hong-kong-economy/article/3300066/hong-kong-government-adopts-chatgpt-style-tool-powered-deepseek?module=top_story&pgtype=homepage",
      "Oriental Daily" : "https://orientaldaily.on.cc/content/%E5%85%A9%E5%B2%B8%E5%9C%8B%E9%9A%9B/odn-20250225-0225_00180_005/%E9%A6%AC%E6%96%AF%E5%85%8B%E4%BF%83%E5%8C%AF%E5%A0%B1%E5%B7%A5%E4%BD%9C--%E5%A4%9A%E9%83%A8%E9%96%80%E7%B1%B2%E5%8B%BF%E8%A6%86"}

configs = {"new statesman" : ["c-featured-image", "src="],
      "daily heil" : ["artSplitter mol-img-group", "src="],
      "CNN" : ["image__lede article__lede-wrapper", "src="],
      "BBC": ["ssrcss-1qlkdz0-ComponentWrapper-FullWidthWrapper ey0461q0", "src="],
      "aljaz" : ["responsive-image", "src=", "https://www.aljazeera.com"],
      "South China News": ["css-0 e1gf69pb3", "src="],
      "Oriental Daily" : ["smallpic", "src=", "https://orientaldaily.on.cc"]}
                                                                    


def find_image(url, config):
    r = requests.get(url=url)

    soup = BeautifulSoup(r.content, "lxml")
    image_section = str(soup.find(class_=config[0]))
    section = image_section.find(config[1])
    try:
        print(config[2] + image_section[section:].split('"')[1])
    except(IndexError):
        print(image_section[section:].split('"')[1])





for key, value in urls.items():
    find_image(value, configs[key])

# find_image(urls["abc"], configs["abc"])
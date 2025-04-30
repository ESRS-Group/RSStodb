import requests


def main(language, text):
    url = "http://51.38.82.118:5323/esrs-translate//translate"

    request = {
        "q": text,
        "source": language,
        "target": "en",
        "format": "text"
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=request, headers=headers, timeout=10)
        response.raise_for_status()
        return (True, response.json().get("translatedText"))
    except requests.exceptions.RequestException as e:
        print (False,  {e})

if __name__ == "__main__":
    main()
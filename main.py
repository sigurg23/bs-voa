import os
import requests
from slugify import slugify
from bs4 import BeautifulSoup

HEADERS = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/75.0.3770.90 Chrome/75.0.3770.90 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9'
}

BASE_URL = "http://www.manythings.org/voa/history/{index}.html"
BASE_PATH = "pages"


def scrap_page(page_number):
    page_url = BASE_URL.format(index=page_number)    
    response = requests.get(page_url, headers=HEADERS)
    if 200 != response.status_code:
        print("Error parsing page: {}".format(page_number))

    soup = BeautifulSoup(response.text, features="html.parser")
    title = soup.find("h1").getText()
    title = title.strip("\'\"")
    title = str(title).encode("utf-8")
    title = slugify(title)

    page_path = "./{}/page_{}".format(BASE_PATH, str(page_number).zfill(3))
    try:
        os.makedirs(page_path)
    except FileExistsError as error:
        pass

    with open("{}/{}.html".format(page_path, title), "w") as file:
        file.write(response.text)

    soup = BeautifulSoup(response.text, features="html.parser")
    for a in soup.find_all("a"):
        link = a["href"]
        if link.endswith("mp3"):
            response_mp3 = requests.get(link, allow_redirects=True)
            open("{}/{}.mp3".format(page_path, title), 'wb').write(response_mp3.content)
            break


for idx in range(0, 251):
    print("Processing page {}...".format(idx))
    scrap_page(idx)

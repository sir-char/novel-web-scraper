from novel_scraper import NovelFull

import requests
import json
import time
from bs4 import BeautifulSoup

def getSoup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def getNewUrl(org_url, novel_page, page_url, page_num = 1):
    novel_url = f"{org_url}{novel_page}{page_url}{page_num}"
    return novel_url

url = "https://novelfull.com"
soup = getSoup(url)
posts = soup.find_all('div', class_="item")

novelSite = NovelFull(url)

data = {}
data['novel'] = []

# Gets list of top novels from home page of NovelFull
with open("json_files/fifth_data.json", "w") as data_file:
    data = novelSite.get_novel_list(data, posts)
    json.dump(data, data_file, indent=3)

page_url = "?page="

# Gets list of chapters from each novel previously scraped
with open("json_files/fifth_data.json", "r+") as data_file:
    data = json.load(data_file)
    start = time.perf_counter()
    data_file.seek(0)
    data = novelSite.get_chapter_list(data, page_url)
    json.dump(data, data_file, indent=3)
    data_file.truncate()

    end = time.perf_counter()

    print(f"Time take is {round(end-start, 3)} second(s).")

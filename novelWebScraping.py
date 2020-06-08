import requests
import json
from bs4 import BeautifulSoup

def getSoup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

url = "https://novelfull.com"

soup = getSoup(url)

posts = soup.find_all('div', class_="item")

data = {}
data['novel'] = []

with open("data.json", "w") as data_file:
    for post in posts:
        title = post.find('a')['title']
        link = post.find('a')['href']
        data['novel'].append({
            "title": title,
            "link": link
        })
    json.dump(data, data_file, indent=3)

with open("data.json", "r+") as data_file:
    data = json.load(data_file)
    for novel in data['novel']:
        new_url = f"{url}{novel['link']}"
        soup = getSoup(new_url)
        # last_page_li = soup.find('li', class_="last")
        # print(last_page_li)
        # last_page = soup.find('a')['data']
        # last_page = int(soup.find('a')['data-*']) + 1
        # print(f"last html page for {novel['title']} is page {last_page}")
        posts = soup.find_all('ul', class_="list-chapter")
        novel['chapters'] = []
        for post in posts:
            for li in post.find_all('li'):
                ch_title = li.find('a')['title']
                ch_link = li.find('a')['href']
                novel['chapters'].append({
                    "chapterTitle": ch_title,
                    "chapterLink": ch_link
                })
    data_file.seek(0)
    json.dump(data, data_file, indent=3)
    # data_file.truncate()

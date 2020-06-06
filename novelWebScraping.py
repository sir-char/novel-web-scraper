import requests
import json
from bs4 import BeautifulSoup

url = "https://novelfull.com"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

posts = soup.find_all('div', class_="item")

data = {}
data['novel'] = []

with open("data.json", "w") as data_file:
    for post in posts:
        title = post.find('a')['title']
        link = post.find('a')['href']
        print(title, link)
        data['novel'].append({
            "title": title,
            "link": link
        })
    json.dump(data, data_file, indent=3)

with open("data.json", "r") as data_file:
    data = json.load(data_file)
    for novel in data['novel']:
        newUrl = f"{url}{novel['link']}"
        respons = requests.get(newUrl)
        soup = BeautifulSoup(respons.text, 'html.parser')
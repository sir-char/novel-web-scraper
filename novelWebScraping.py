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

with open("fourth_data.json", "w") as data_file:
    # for post in posts:
    #     title = post.find('a')['title']
    #     link = post.find('a')['href']
    #     data['novel'].append({
    #         "title": title,
    #         "link": link
    #     })
    data = novelSite.get_novel_list(data, posts)
    json.dump(data, data_file, indent=3)

page_url = "?page="

with open("fourth_data_DO_NOT_TOUCH.json", "r+") as data_file:
    data = json.load(data_file)
    start = time.perf_counter()
    # for novel in data['novel']:
    #     i = 0
    #     soup = getSoup(getNewUrl(url, novel['link'], page_url))
    #     last_page_li = soup.find('li', class_="last")
    #     last_page = int(last_page_li.find('a', attrs={'data-page' : True})['data-page']) + 1
    #     print(f"last html page for {novel['title']} is page {last_page}")
    #     novel['chapters'] = []
    #     for page in range(1, last_page):
    #         if page != 1: 
    #             soup = getSoup(getNewUrl(url, novel['link'], page_url, page))
    #         print("page is " + str(page))
    #         posts = soup.find_all('ul', class_="list-chapter")
    #         for post in posts:
    #             for li in post.find_all('li'):
    #                 # if i >= 15:
    #                 #     break
    #                 ch_title = li.find('a')['title']
    #                 ch_link = li.find('a')['href']
    #                 print(ch_title, ch_link)
    #                 novel['chapters'].append({
    #                     "chapterTitle": ch_title,
    #                     "chapterLink": ch_link
    #                 })
    #                 i += 1
    data_file.seek(0)
    data = novelSite.get_chapter_list(data, page_url)
    json.dump(data, data_file, indent=3)
    # data_file.truncate()

    end = time.perf_counter()

    print(f"Time take is {round(end-start, 3)} second(s).")

from novel_scraper import NovelFull

import requests
import json
import time
import concurrent.futures
from bs4 import BeautifulSoup
from urllib3.exceptions import HTTPError
# from urllib3.exceptions import ProtocolError

def getSoup(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def get_new_url(org_url, chapter_url):
    novel_url = f"{org_url}{chapter_url}"
    return novel_url

def scrape_chapter(chapter):
    try:
        print(f"Scraping {novel['title']} {chapter['chapterTitle']}...")
        chapter['content'] = []
        soup = getSoup(get_new_url(url, chapter['chapterLink']))
        if soup.find('div', class_="cha-words"):
            title = soup.find('div', id="chapter-content")
            chapter_cont = soup.find('div', class_="cha-words")
            for string in title.find_all('p'):
                chapter['content'].append(string.getText())
                # print(string.getText())
            for paragraph in chapter_cont.find_all('p'):
                chapter['content'].append(paragraph.getText())
        else:
            chap_content = soup.find('div', id="chapter-content")
            for paragraph in chap_content.find_all('p'):
                chapter['content'].append(paragraph.getText())
        i += 1
    except HTTPError as e:
        print(e)
    # return


url = "https://novelfull.com"
# header = {'User-Agent': 'Mozilla/5.0'}
# /reincarnation-of-the-strongest-sword-god/chapter-1-starting-over.html"
soup = getSoup(url)

novelSite = NovelFull(url)

# Don't remember why this is here exactly
with open("json_files/fifth_data.json", "r") as data_file:
    data = json.load(data_file)

# Scrapes the contents of every chapter in each novel
with open("json_files/fifth_data.json", "w") as data_file:
    start = time.perf_counter()
    print("Starting scrape.")
    chapters_per_novel = []
    total_chapters = 0
    for novel in data['novel']:
        i = 0
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(scrape_chapter, novel['chapters']) #for chapter in novel['chapters']

        # for chapter in novel['chapters']:
        #     if i >= 15: break
            
        # chapters_per_novel.append(i)
        # total_chapters += i
    
    # i = 0
    # for novel in data['novel']:
    #     print(f"{chapters_per_novel[i]} chapters scraped for {novel['title']}")
    #     i += 1

    end = time.perf_counter()
    print(f"Time take is {round(end-start, 3)} second(s).")
    # print(f"Time taken to scrape {total_chapters} chapters for {len(data['novel'])} novels is {end - start} seconds.")

    data_file.seek(0)
    json.dump(data, data_file, indent=3)
            # for paragraph in p_list:
                # print(paragraph, "\n")
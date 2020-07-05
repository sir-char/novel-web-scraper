import requests
import json
import concurrent.futures
from bs4 import BeautifulSoup

class NovelFull:
    def __init__(self, url):
        self.url = url

    def get_novel_list(self, data, posts):
        for post in posts:
            title = post.find('a')['title']
            link = post.find('a')['href']
            data['novel'].append({
                "title": title,
                "link": link
            })
        return data

    def update_novel_list(self, file_name):
        pass

    def get_chapter_list(self, json_obj, page_url):
        # Looping through each object in json_obj
        for novel in json_obj['novel']:
            i = 0
            soup = get_soup(get_novel_url(novel['link'], page_url))
            last_page_li = soup.find('li', class_="last")
            last_page = int(last_page_li.find('a', attrs={'data-page' : True})['data-page']) + 1
            # print(f'Last HTML page for {novel['title']} is page {last_page})
            novel['chapters'] = []
            for page in range(1, last_page + 1):
                soup = get_soup(get_novel_url(novel['link'], page_url, page))
                # print(f'Page: {str(page)}')
                posts = soup.find_all('ul', class_='list-chapter')
                for post in posts:
                    for li in post.find_all('li'):
                        # if i >= 15:
                        #     break
                        ch_title = li.find('a')['title']
                        ch_link = li.find('a')['href']
                        print(ch_title, ch_link)
                        novel['chapters'].append({
                            "chapterTitle": ch_title,
                            "chapterLink": ch_link
                        })
                        i += 1
        return json_obj

    def update_chapter_list(self):
        pass

    # Scrape all chapters of a given novel
    def get_chapters(self):
        pass

    def get_new_chapters(self):
        pass

    # Scrape a single specific chapter
    def get_chapter(self):
        pass

    def get_novel_url(self, novel_url, page_url, page_num=1):
        return f'{self.url}{novel_url}{page_url}{page_num}'

    def get_chapter_url(self, chapter_url):
        return f'{self.url}{chapter_url}'

    def get_soup(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

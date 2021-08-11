import requests
import json
import concurrent.futures
from bs4 import BeautifulSoup

class NovelFull:
    def __init__(self, url):
        self.url = url

    def get_novel_url(self, novel_url, page_url, page_num=1):
        return f'{self.url}{novel_url}{page_url}{page_num}'

    def get_chapter_url(self, chapter_url):
        return f'{self.url}{chapter_url}'

    def get_soup(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    # Gets the list of novels from website
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

    # TODO make this get the chapter list for a specific novel
    # Gets the list of chapters for each novel
    def get_chapter_list(self, json_obj, page_url):
        # Looping through each object in json_obj
        for novel in json_obj['novel']:
            i = 0
            soup = self.get_soup(self.get_novel_url(novel['link'], page_url))
            last_page_li = soup.find('li', class_="last")
            last_page = int(last_page_li.find('a', attrs={'data-page' : True})['data-page']) + 1
            # print(f'Last HTML page for {novel['title']} is page {last_page})
            novel['chapters'] = []
            for page in range(1, last_page + 1):
                soup = self.get_soup(self.get_novel_url(novel['link'], page_url, page))
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

    # TODO figure out how to implement this
    # Scrape a single specific chapter
    def get_chapter(self, chapter):
        pass
        # print(f"Scraping {novel['title']} {chapter['chapterTitle']}...")
        # chapter['content'] = []
        # soup = self.get_soup(self.get_chapter_url(url, chapter['chapterLink']))
        # if soup.find('div', class_="cha-words"):
        #     title = soup.find('div', id="chapter-content")
        #     chapter_cont = soup.find('div', class_="cha-words")
        #     for string in title.find_all('p'):
        #         chapter['content'].append(string.getText())
        #         # print(string.getText())
        #     for paragraph in chapter_cont.find_all('p'):
        #         chapter['content'].append(paragraph.getText())
        # else:
        #     chap_content = soup.find('div', id="chapter-content")
        #     for paragraph in chap_content.find_all('p'):
        #         chapter['content'].append(paragraph.getText())
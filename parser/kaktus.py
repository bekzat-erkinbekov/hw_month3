from pprint import pprint
import datetime
import requests
from bs4 import BeautifulSoup

today = str(datetime.datetime.today())[:10:]


# def get_html(url):
#     req = requests.get(url, headers=HEADERS)
#     return req
#
# def get_data(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     items = soup.find_all("div", class_="ArticleItem--data ArticleItem--data--withImage")
#     news = []
#
#     for item in items:
#             new = {
#                 'title': item.find('a', class_="ArticleItem--name").string.replace('\n', ''),
#                 'photo': item.find("a", class_="ArticleItem--image").find('img').get('src'),
#                 'link': item.find('a', class_="ArticleItem--name").get('href'),
#                 'time': item.find('div', class_='ArticleItem--time').string.replace('\n', '')
#             }
#             news.append(new)
#     return news
# def news_parser():
#     html = get_html(URL)
#     if html.status_code == 200:
#         news = []
#         html = get_html(URL)
#         new = get_data(html.text)
#         news.extend(new)
#
#         return news
#     else:
#         raise Exception("Error in parser!")

class Parser:
    def __init__(self, url):
        self.__url = url

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        self.__url = value

    global HEADERS

    HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0"}

    def get_html(self):
        self.__req = requests.get(url=self.__url, headers=HEADERS)
        return self.__req

    def get_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all("div", class_="ArticleItem--data ArticleItem--data--withImage")
        news = []

        for item in items:
            new = {
                'title': item.find('a', class_="ArticleItem--name").string.replace('\n', ''),
                'photo': item.find("a", class_="ArticleItem--image").find('img').get('src'),
                'link': item.find('a', class_="ArticleItem--name").get('href'),
                'time': item.find('div', class_='ArticleItem--time').string.replace('\n', '')
            }
            news.append(new)
        return news


URL = f"https://kaktus.media/?lable=8&date={today}&order=time"

def new_parser():
    html = Parser(URL)
    if html.get_html().status_code == 200:
        news = []
        html2 = html.get_html()
        new = html.get_data(html2.text)
        news.extend(new)

        return news
    else:
        raise Exception("Error in parser!")
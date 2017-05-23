#抓取豆瓣详情页的电影名称、评分、IMDb链接、导演和常用的tag

import requests
from bs4 import BeautifulSoup
import re

# 给定一个url页面
URL = 'https://movie.douban.com/subject/5133063/'

def scawler(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers = headers)
    if response.status_code != 200:
        raise ValueError('scawl error, http code: %s' % response.status_code)
    return response.text

def analysis_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    title = soup.title.string #拿出了title
    rating_num = soup.strong.string #拿出了评分
    info = soup.find_all('div', id='info') #拿出了info，但是怎么拿出来IMDb链接和导演呢？？？？？
    tags_html = soup.find('div', class_='tags-body')
    tags = tags_html.find_all('a')
    for tag in tags:
        tag1 = tag.string
        print(tag1)

    #tags_soup = BeautifulSoup(tags, 'html.parser')
    #tags = soup.a.string
    #print(tag1)
    #info_soup = BeautifulSoup(info, 'html.parser')
    #imdb_link = info_soup.span
    #print(title, rating_num,imdb_link)


if __name__ == '__main__':
    analysis_html(scawler(URL))

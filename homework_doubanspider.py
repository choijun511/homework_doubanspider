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
    #拿出了title
    title = soup.title.string

    #拿出了评分
    rating_num = soup.strong.string

    #拿出了info，但是怎么拿出来IMDb链接和导演呢？？？？？
    info = soup.find('div', id='info')
    IMDb_link = 'http://www.imdb.com/title/' + info.find_all('a').pop().string
    #print(IMDb_link)

    #拿出了tags，并且把他们装到了一个数组里面
    tags_html = soup.find('div', class_='tags-body')
    tags = tags_html.find_all('a')
    tag_array = []
    for tag in tags:
        tag_array.append(tag.string)
    return(title, rating_num, IMDb_link, tag_array)

    #tags_soup = BeautifulSoup(tags, 'html.parser')
    #tags = soup.a.string
    #print(tag1)
    #info_soup = BeautifulSoup(info, 'html.parser')
    #imdb_link = info_soup.span
    #print(title, rating_num,imdb_link)


if __name__ == '__main__':
    analysis_html(scawler(URL))

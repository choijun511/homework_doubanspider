#抓取豆瓣详情页的电影名称、评分、IMDb链接、导演和常用的tag

#coding=utf-8

import requests
from bs4 import BeautifulSoup
import re

from config import DB_USER, DB_PASSWD
import pymysql

db = pymysql.connect('127.0.0.1', port=3306, user=DB_USER,
        passwd=DB_PASSWD, db='doubanmovie', charset='UTF8')
cursor = db.cursor()

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

    #拿出了info，并从info中拿出了IMDb链接和导演
    info = soup.find('div', id='info')
    IMDb_link = 'http://www.imdb.com/title/' + info.find_all('a').pop().string
    #print(IMDb_link）
    director = info.find('span')
    director_name_array = []
    director_name = director.find_all('a')
    for director_name in director_name:
        director_name_array.append(director_name.string)
    director_name_string = ', '.join(director_name_array)
    #print(director_name_string)

    #拿出了tags，并且把他们装到了一个数组里面
    tags_html = soup.find('div', class_='tags-body')
    tags = tags_html.find_all('a')
    tag_array = []
    for tag in tags:
        tag_array.append(tag.string)
    tag_string = ', '.join(tag_array)
    return([title, rating_num, IMDb_link, director_name_string, tag_string])

def save_db(data):
    sql = 'insert into doubanmovie (title, rating_num, IMDb_link, director_name_string, tag_string) values (%s, %s, %s, %s, %s)'
    cursor.execute(sql, data)
    db.commit()

if __name__ == '__main__':
    result = scawler(URL)
    data = analysis_html(result)
    save_db(data)

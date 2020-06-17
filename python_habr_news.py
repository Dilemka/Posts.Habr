# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
import codecs
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
engine = create_engine('sqlite:///my.db', echo = True)
from sqlalchemy.ext.declarative import declarative_base


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestEception, ValueError):
        print("Сетевая ошибка")
        return False

def get_habr_news(html):

    soup = BeautifulSoup(html, "html.parser")
    all_news = soup.findAll("article", class_="post post_preview")
    result_all_news = []

    for news in all_news:
    
        title = news.find("a", class_= "post__title_link").text
        avtor = news.find("span", class_= "user-info__nickname user-info__nickname_small").text
        url = news.find("a", class_= "post__title_link")["href"]
        result_all_news.append({
            "title": title,
            "avtor": avtor,
            "url": url
        })
    return result_all_news

# def write_news_csv(res):

    # for new_post in res:
    #     post = Post(new_post['title'], new_post['avtor'], new_post['url'])
    #     writer = csv.DictWriter(f, post)
    #     writer.writerow(new_post)
    #     # for all in res:
    #     #     fields = ['title', 'avtor', "url"]
    #     #     writer = csv.DictWriter(f, fields, delimiter=";")
    #     #     # writer.writeheader()
    #     #     writer.writerow(all)

Base = declarative_base()

class Post(Base):
    __tablename__ = 'Post_habr'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)
   
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()

def write_news_csv(res):
    for new_post in res:
        p1 = Post(new_post['title'], new_post['avtor'], new_post['url'])
        
    session.add(p1)
    session.commit()

if __name__ == "__main__":
    html = get_html("https://www.habr.com/ru/all/") 
    if html:
        get_habr_news(html)
        res = get_habr_news(html)
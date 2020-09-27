import requests
from bs4 import BeautifulSoup
import sqlite3


def get_links():
    url = 'https://slova.org.ru/top_poems.html'
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')
    links_list = []
    for link in soup.select('#stihi_list > a'):
        links_list.append(link['href'])
    return links_list


def generation_poems(links_list):
    list_poems = []
    for link in links_list:
        url = 'https://slova.org.ru' + link
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')
        author = soup.select_one('body > div.header > span > a').text
        title = soup.select_one('body > div.content > div.main_column > div > h3').text
        poem = soup.select_one('body > div.content > div.main_column > div > pre').text
        list_poems.append((author, title, poem))
    return list_poems


def generation_database():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute(""" CREATE TABLE list_poems (author text, title text, poem text) """)
    list_poems = generation_poems(get_links())
    cursor.executemany("INSERT INTO list_poems VALUES (?, ?, ?)", list_poems)
    conn.commit()


def get_random_poem_from_database():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    poem = cursor.execute("SELECT * FROM list_poems ORDER BY RANDOM() LIMIT 1").fetchall()[0]
    poem = f'{poem[0]}\n\n{poem[1]}\n{poem[2]}'
    return poem


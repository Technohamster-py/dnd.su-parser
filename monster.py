import os
from bs4 import BeautifulSoup
import requests
from lxml import etree

class Monster:
    def __init__(self, url):


    def parse(self, url):
        page = requests.get(url)
        if not page.status_code == 200:
            return None
        soup = BeautifulSoup(page.text, 'html.parser')

        card_title = soup.find_all('h2', class_='card-title')[0].find('span').text
        self.name = card_title.split('[')[0]
        self.name_eng = card_title.split('[')[1].split(']')[0]

        card_content = soup.find('ul', class_='params card__article-body', recursive=True).find_all('li', recursive=False)

        self.size = card_content[0].text.split('<sup>')[0]
        self.type = card_content[0].text.split('</sup>')[1].split(',')[0]
        self.aligment = card_content[0].text.split('</sup>')[1].split(',')[1]
        self.ac = card_content[1].text.split('</strong>')[1]
        self.max_hp = card_content[2].find_all('span')[0].text
        self.formula = f"{card_content[2].find_all('span')[0].text}d{card_content[2].find_all('span')[2].text}"
        self.speed = card_content[1].text.split('</strong>Скорость</strong>')[1]

        stat_table = card_content[1].find_all('div', class_='stat')
        self.stats = {
            'STR': stat_table[0].find_all('div')[0].text.split(' ')[0],
            'DEX': stat_table[0].find_all('div')[1].text.split(' ')[0],
            'CON': stat_table[0].find_all('div')[2].text.split(' ')[0],
            'INT': stat_table[0].find_all('div')[3].text.split(' ')[0],
            'WIS': stat_table[0].find_all('div')[4].text.split(' ')[0],
            'CHA': stat_table[0].find_all('div')[5].text.split(' ')[0]
        }


import os
from bs4 import BeautifulSoup
import requests


class Spell:
    def __init__(self, url):
        self.title = ''
        self.title_eng = ''
        self.components = {'verbal': False, 'somatic': False, 'material': ''}
        self.description = ''
        self.classes = []
        self.school = ''
        self.level = 0
        self.range = 0
        self.source = 'PHB'
        self.time = ''
        self.duration = ''
        self.parse(url)

    def __str__(self) -> str:
        return f"{self.title} - {self.title_eng}"

    def parse(self, url):
        page = requests.get(url)
        if not page.status_code == 200:
            return None
        soup = BeautifulSoup(page.text, 'html.parser')
        card_title = soup.find_all('h2', class_='card-title')[0].find('span').text
        self.title = card_title.split('[')[0]
        self.title_eng = card_title.split('[')[1].split(']')[0]

        card_content = soup.find('ul', class_='params card__article-body', recursive=True).find_all('li', recursive=False)
        self.level = card_content[0].text.split(' уровень, ')[0]
        self.school = card_content[0].text.split(' уровень, ')[1]

        self.time = card_content[1].text.split('/strong>')[1]
        self.range = card_content[2].text.split('/strong>')[1]

        if '(' in card_content[3].text.split('/strong>')[1]:
            material = card_content[3].text.split('/strong>')[1].split('(')[1].split(')')[0]
        else:
            material = ''
        somatic = 'С, ' in card_content[3].text.split('/strong>')[1]
        verbal = 'В, ' in card_content[3].text.split('/strong>')[1]
        self.components['verbal'] = verbal
        self.components['somatic'] = somatic
        self.components['material'] = material

        self.duration = card_content[4].text.split('/strong>')[1]

        self.classes = card_content[5].text.split('/strong>')[1]

        self.source = card_content[6].text.split('/strong>')[1]

        self.description = card_content[7].text.split('/strong>')[1]

    def save_to_file(self, file_name=""):
        if file_name == "":
            file_name = f"{self.title_eng}_spell.xml"
        if not os.path.exists(f"{os.getcwd()}/downloads/spells"):
            os.makedirs(f"{os.getcwd()}/downloads/spells")
        full_path = f"{os.getcwd()}/downloads/spells/{file_name}"
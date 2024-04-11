import os
from bs4 import BeautifulSoup
import requests
from lxml import etree


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

        self.classes = [i for i in card_content[5].text.split('/strong>')[1].split(',')]

        self.source = card_content[6].text.split('/strong>')[1]

        self.description = card_content[7].text

    def save_to_file(self, file_name=""):
        if file_name == "":
            file_name = f"{self.title_eng}_spell.xml"
        if not os.path.exists(f"{os.getcwd()}/downloads/spells"):
            os.makedirs(f"{os.getcwd()}/downloads/spells")
        full_path = f"{os.getcwd()}/downloads/spells/{file_name}"

        root = etree.Element('spell')

        title = etree.SubElement(root, 'title').text = self.title
        level = etree.SubElement(root, 'level').text = self.level
        school = etree.SubElement(root, 'school').text = self.school

        classes = etree.SubElement(root, 'classes')
        for cls in self.classes:
            etree.SubElement(classes, 'class').text = cls

        range_element = etree.SubElement(root, 'range').text = self.range
        casting_time = etree.SubElement(root, 'casting-time').text = self.time
        duration = etree.SubElement(root, 'duration').text = self.duration

        components = etree.SubElement(root, 'components')
        verbal = etree.SubElement(components, 'verbal').text = self.components['verbal']
        somatic = etree.SubElement(components, 'somatic').text = self.components['somatic']
        material = etree.SubElement(components, 'material').text = self.components['material']

        description = etree.SubElement(components, 'description').text = self.description

        tree = etree.ElementTree(root)

        tree.write(full_path, xml_declaration=False, encoding='utf-8')
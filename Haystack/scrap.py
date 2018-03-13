import requests
from bs4 import BeautifulSoup
import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gogov.settings')
django.setup()

from search.models import MainData

with open('malsapro/crawled.txt') as fp:
    main_soup = BeautifulSoup(fp, "html.parser")

lines = fp.readline()

for line in lines:
    r = requests.get(line)
    soup = BeautifulSoup(r.content, "html.parser")
    keywords = soup.find('meta', {'name': 'keywords'})
    description = soup.find('meta', {'name': 'description'})
    title = soup.find('title')
    main_heading = soup.findAll('h1')
    paragraphs = soup.findAll('p')


get_url = MainData.objects.values('url')
new_url = list(get_url)

if page_url not in new_url:
    def add_data():
        model_con = MainData.objects.create(url=page_url)
        try:
            model_con.title = title.text
        except (TypeError, AttributeError):
            pass

        try:
            model_con.metadata = description.text
        except (TypeError, AttributeError):
            pass

        try:
            model_con.meta_keywords = keywords.text
        except (TypeError, AttributeError):
            pass

        try:
            model_con.context = main_heading.text + paragraphs.text
        except (TypeError, AttributeError):
            pass

        model_con.save()
    add_data()
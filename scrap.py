import requests
from bs4 import BeautifulSoup
import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gogov.settings')
django.setup()

from search.models import MainData

def readFile(filename):
    filehandle = open(filename)
    lines = filehandle.readlines()

    for line in lines:
        one_before_final_line = line.split('\n')
        final_line = one_before_final_line[0]
        r = requests.get(final_line)
        print(final_line)
        soup = BeautifulSoup(r.content, "html.parser")
        keywords = soup.find('meta', {'name': 'Keywords'})
        description = soup.find('meta', {'name': 'Description'})
        title = soup.find('title')
        main_heading = soup.findAll('h1')
        paragraphs = soup.findAll('p')

        get_url = MainData.objects.values('url')
        new_url = list(get_url)

        final_context = ''
        for paragraph in paragraphs:
            final_context += paragraph.text
        for heading in main_heading:
            final_context += heading.text

        if final_line not in new_url:
            def add_data():
                model_con = MainData.objects.create(url=final_line)
                try:
                    model_con.title = title.text
                except (TypeError, AttributeError):
                    pass

                try:
                    model_con.context = final_context
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

                model_con.save()

            add_data()

    filehandle.close()

fileDir = os.path.dirname(os.path.realpath('__file__'))

filename = os.path.join(fileDir, 'mygov/crawled.txt')
readFile(filename)
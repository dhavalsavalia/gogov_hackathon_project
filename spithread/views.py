from django.shortcuts import render
from .forms import MainProjectForm
from django.http import HttpResponse

import threading
from queue import Queue
from spithread.helpers.spider import Spider
from spithread.helpers.domain import *
from spithread.helpers.general import *


def index(request):

    form = MainProjectForm()

    if request.method == 'POST':
        form = MainProjectForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            form.save()

            PROJECT_NAME = str(request.POST['PROJECT_NAME'])
            HOMEPAGE = str(request.POST['HOMEPAGE'])

            PROJECT_NAME_APP = PROJECT_NAME
            HOMEPAGE_APP = HOMEPAGE
            DOMAIN_NAME = get_domain_name(HOMEPAGE_APP)
            QUEUE_FILE = PROJECT_NAME_APP + '/queue.txt'
            CRAWLED_FILE = PROJECT_NAME_APP + '/crawled.txt'
            NUMBER_OF_THREADS = 8
            queue = Queue()
            Spider(PROJECT_NAME_APP, HOMEPAGE_APP, DOMAIN_NAME)

            # Create worker threads (will die when main exits)
            def create_workers():
                for _ in range(NUMBER_OF_THREADS):
                    t = threading.Thread(target=work)
                    t.daemon = True
                    t.start()

            # Do the next job in the queue
            def work():
                while True:
                    url = queue.get()
                    Spider.crawl_page(threading.current_thread().name, url)
                    queue.task_done()

            # Each queued link is a new job
            def create_jobs():
                for link in file_to_set(QUEUE_FILE):
                    queue.put(link)
                queue.join()
                crawl()

            # Check if there are items in the queue, if so crawl them
            def crawl():
                queued_links = file_to_set(QUEUE_FILE)
                if len(queued_links) > 0:
                    print(str(len(queued_links)) + ' links in the queue')
                    create_jobs()

            create_workers()
            crawl()

            # Adding data to database, i.e. PostgreSQL/SQLite
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

            crawled_file = PROJECT_NAME_APP + '/crawled.txt'

            filename = os.path.join(fileDir, crawled_file)
            readFile(filename)

            # Updating the index in Elasticsearch server
            os.system("python manage.py update_index")

            return HttpResponse('We have started crawled the website and done everything you need.')
        else:
            return HttpResponse('Something went wrong while submitting the URL, please check again?')

    return render(request, 'index.html', {'form': form})

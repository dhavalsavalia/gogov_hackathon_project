import os
from time import sleep

os.system("python manage.py rebuild_index")
sleep(1)
os.system("y")

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ndslsaver.settings")
import django
django.setup()
from parsing_data.models import ParsingData
from data.db import DBConnect
from scrap.scrapy import get_realpath
from scrap.test import test
# title, link, author, abstract, content
if __name__ == '__main__':
    get_realpath('웹마케팅')
    # link = test()
    # print(link)
    # test()
    #ParsingData(title=t, link=l).save()
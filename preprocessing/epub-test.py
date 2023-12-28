import ebooklib
from ebooklib import epub
import re
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
from multiprocessing import Pool
from functools import partial
import glob
from datetime import datetime as dt
from dateutil.parser import parse


book = epub.read_epub("../dump/1test.epub")


print(book.get_metadata('DC', 'title')[0][0])
print(book.get_metadata('DC', 'creator')[0][0])

metadata = book.get_metadata('DC', 'date')

publishdate = parse('3000-01-01').replace(tzinfo=None)

for date in metadata:
    d = parse(date[0], fuzzy=True).replace(tzinfo=None)
    if d < publishdate:
        publishdate = d


print(publishdate)


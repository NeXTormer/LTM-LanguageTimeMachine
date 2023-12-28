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
import json
import csv

# book = epub.read_epub("../dump/1test.epub")


def extract_data(file):
    data = {}

    if file.endswith('.html'):
        with open(file, 'r') as html:
            soup = BeautifulSoup(html.read(), 'html.parser')
            text_content = soup.get_text(separator=' ', strip=True)
            data['text'] = text_content
            data['type'] = 'HTML'

    elif file.endswith('.epub'):
        try:
            book = epub.read_epub(file)
            raw_text = ""

            dates = book.get_metadata('DC', 'date')
            publish_year = 3000

            if len(dates) == 2:
                d1 = parse(dates[0][0], fuzzy=True).replace(tzinfo=None)
                d2 = parse(dates[1][0], fuzzy=True).replace(tzinfo=None)

                if d1.year == d2.year and d1.month == d2.month and abs(d1.day - d2.day) < 2:
                    publish_year = min(d1.year, d2.year)

            title = book.get_metadata('DC', 'title')[0][0]

            try:
                author = book.get_metadata('DC', 'creator')[0][0]
            except:
                author = ''

            data['date_metadata'] = publish_year
            data['title'] = title
            data['author'] = author
            data['type'] = 'ePub'

            for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
                soup = BeautifulSoup(item.get_content().decode('utf-8', 'ignore'), 'html.parser')
                text_content = soup.get_text(separator=' ', strip=True)
                raw_text += text_content + ' '

            # Remove extra whitespaces
            raw_text = re.sub(r'\s+', ' ', raw_text).strip()

            data['text'] = raw_text

        except Exception as e:
            print("Failed to process: ", file)
            print(e)
            return None

    return data


if __name__ == "__main__":

    directory = '../dump/'

    enable_multithreading = True

    epub_files = [file for file in tqdm(os.listdir(directory), desc='generate file list') if file.endswith('.epub') or file.endswith('.html')]
    file_paths = [os.path.join(directory, file) for file in tqdm(epub_files, desc='generate file paths')]

    pbar = tqdm(total=len(file_paths), desc='Processing files', position=0, leave=True)

    results = []
    a = 0

    if not enable_multithreading:
        for path in tqdm(file_paths, desc='Processing EPUBs ST'):
            results.append(extract_data(path))
            a += 1
            if a > 10:
                break

    if enable_multithreading:
        with Pool() as pool:
            results = pool.imap_unordered(extract_data, file_paths, chunksize=8)

            with open("/Volumes/Untitled/all_data.csv", "w", newline='') as text_file:
                writer = csv.DictWriter(text_file, fieldnames=['title', 'author', 'type', 'date_metadata', 'text'])
                writer.writeheader()
                for result in results:
                    pbar.update(1)
                    if result is not None:
                        writer.writerow(result)

    pbar.close()

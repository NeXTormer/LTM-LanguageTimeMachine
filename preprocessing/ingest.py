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
import nltk
nltk.download('words')

from nltk.corpus import words


check_word_length_cutoff = 3

all_words_list = words.words()
all_words_list = [word for word in all_words_list if len(word) <= check_word_length_cutoff]

chunk_size = 2000


def extract_data(file):
    data = {}

    try:
        book = epub.read_epub(file)
        raw_text = ""

        dates = book.get_metadata('DC', 'date')
        publish_year = 3000
        skip_year_search = False

        if len(dates) == 2:
            d1 = parse(dates[0][0], fuzzy=True).replace(tzinfo=None)
            d2 = parse(dates[1][0], fuzzy=True).replace(tzinfo=None)

            if d1.year == d2.year and d1.month == d2.month and abs(d1.day - d2.day) < 2:
                publish_year = min(d1.year, d2.year)
                skip_year_search = True

        title = book.get_metadata('DC', 'title')[0][0]

        try:
            author = book.get_metadata('DC', 'creator')[0][0]
        except:
            author = ''

        data['title'] = title
        data['author'] = author

        parsed_first_page = False
        no_date_found = False
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            if no_date_found:
                break

            if 'item' in item.id:
                soup = BeautifulSoup(item.get_content().decode('utf-8', 'ignore'), 'html.parser')
                text_content = soup.get_text(separator=' ', strip=True)
                raw_text += text_content + ' '

            else:
                if not parsed_first_page and not skip_year_search:
                    soup = BeautifulSoup(item.get_content().decode('utf-8', 'ignore'), 'html.parser')
                    text_content = soup.get_text(separator=' ', strip=True)

                    numbers = re.findall(str("\\s[1-2][7-9]\\d\\d\\s"), str(title + text_content)[:500])

                    for number in numbers:
                        number = int(number)
                        if number < 2023 and number < publish_year:
                            publish_year = number

                    parsed_first_page = True

                    if publish_year == 3000:
                        no_date_found = True

        data['date'] = str(publish_year)

        # Remove extra whitespaces
        raw_text = re.sub(r'\s+', ' ', raw_text).strip()

        # remove everything but words and spaces
        raw_text_only_text = re.sub(r'[^a-zA-Z ]+', '', raw_text).strip().lower()

        if data['date'] == str(3000) or len(raw_text) < 5000 or len(raw_text_only_text) < 1000:
            return None
        text_ratio = len(raw_text_only_text) / len(raw_text)


        raw_text_only_text_only_read_words = [word for word in raw_text_only_text.split() if len(word) > check_word_length_cutoff or word in all_words_list]


        # text_chunks = [raw_text_only_text_only_read_words[i:i + chunk_size] for i in range(0, len(raw_text_only_text_only_read_words), chunk_size)]


        data['text_ratio'] = text_ratio
        data['text'] = " ".join(raw_text_only_text_only_read_words)  # [" ".join(chunk) for chunk in text_chunks]

    except Exception as e:
        print("Failed to process: ", file)
        print(e)
        return None


    return data


if __name__ == "__main__":

    directory = '/home/felix/Dev/zim-extraction/dump/'

    enable_multithreading = True

    epub_files = [file for file in tqdm(os.listdir(directory), desc='generate file list') if file.endswith('.epub')]
    file_paths = [os.path.join(directory, file) for file in tqdm(epub_files, desc='generate file paths')]


    pbar = tqdm(total=len(file_paths), desc='Processing EPUBs', position=0, leave=True)

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

            with open("dataset.json", "w") as text_file:
                text_file.write('[')
                for result in results:
                    pbar.update(1)
                    if result is not None:
                        text_file.write(json.dumps(result) + ',')

                text_file.seek(text_file.tell() - 1)
                text_file.write(']')

    pbar.close()

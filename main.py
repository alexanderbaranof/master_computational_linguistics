import logging
import string
import json
from collections import Counter

import pandas as pd
import pymorphy2
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

# Set up config
SAVE_FIRST_TASK_PATH = './results/task_1/freq_dict.csv'
PAGE_TO_PARSE = 'http://lib.ru/POEZIQ/PESSOA/lirika.txt'
SAVE_SECOND_TASK_PATH = './data/lirika.txt'
LIST_JSON_PATH = './results/task_2/dictionary.json'
LEMMAS_WITH_TWO_LETTERS_O_PATH = './results/task_2/LEMMAS_WITH_TWO_LETTERS_O.txt'


def remove_punctuation(text: str) -> str:
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text


def task_one(file_path: str) -> list:
    # Open file
    f = open(file_path, 'r')
    # Read all text from file
    text = f.read()
    # Close file
    f.close()
    # Apply lowercase
    text = text.lower()
    # Remove punctuation
    text = remove_punctuation(text)
    # Some preprocessing
    text = text.replace('\n', '')
    text = text.replace('\t', '')
    # Tokenize text
    tokens = text.split(' ')
    # Calculate frequency
    freq = Counter(tokens)
    # Save to csv
    df = pd.DataFrame(columns=['word', 'count'])
    df['word'] = freq.keys()
    df['count'] = freq.values()
    df.to_csv(SAVE_FIRST_TASK_PATH)
    return tokens


def task_two(tokens: list) -> None:
    # List for save lemmas with two letters o
    lemmas_with_two_letters_o = list()
    # Create morph analyzer
    morph = pymorphy2.MorphAnalyzer()
    # Going through all the tokens
    for token in set(tokens):
        pv = morph.parse(token)
        normal_form = str(pv[0].normal_form)
        # Lemmas with two letters o
        if normal_form.count('о') == 2:
            lemmas_with_two_letters_o.append(normal_form)
    # Save the result
    f = open(LEMMAS_WITH_TWO_LETTERS_O_PATH, 'w')
    for token in lemmas_with_two_letters_o:
        f.write(token + '\n')
    f.close()

    # Get page from internet
    r = requests.get(PAGE_TO_PARSE)
    # Check answer
    if r.status_code != 200:
        raise Exception('There was a problem getting the page.')
    # Create parser
    bs_parser = BeautifulSoup(r.text, 'html.parser')
    # Extract content
    page_text = bs_parser.get_text()
    # Some preprocessing
    page_text = page_text.replace('\n', '')
    page_text = page_text.lower()
    page_text = remove_punctuation(page_text)
    # Tokenize text and drop duplicates
    text_lirika = list(set(page_text.split(' ')))
    # Save result to json file
    with open(LIST_JSON_PATH, 'w') as fp:
        json.dump(text_lirika, fp)


def main():
    logger = logging.getLogger()
    logger.info('Program started')

    logger.info('Task 1 start')
    tokens = task_one(file_path='./data/dom.txt')
    logger.info('Task 1 done')

    logger.info('Task 2 start')
    task_two(tokens=tokens)
    logger.info('Task 2 done')

    logger.info('Program has finished working')


if __name__ == '__main__':
    main()

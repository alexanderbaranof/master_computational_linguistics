import logging
import string
from collections import Counter

import pandas as pd

logging.basicConfig(level=logging.INFO)


def remove_punctuation(text: str) -> str:
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text


def task_one(file_path: str) -> None:
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
    # Tokenize text
    tokens = text.split(' ')
    # Calculate frequency
    freq = Counter(tokens)
    # Save to csv
    df = pd.DataFrame(columns=['word', 'count'])
    df['word'] = freq.keys()
    df['count'] = freq.values()
    df.to_csv('./results/task_1/freq_dict.csv')


def task_two():
    pass


def main():
    logger = logging.getLogger()
    logger.info('Program started')

    task_one('./data/dom.txt')
    logger.info('Task 1 Done')


if __name__ == '__main__':
    main()

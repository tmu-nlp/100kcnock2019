import itertools
from typing import Generator

from knock50 import extract_sentence


def extract_word(filename: str = './nlp.txt') -> Generator[str, None, None]:
    """
    単語ごとに返す
    """
    for sentence in extract_sentence(filename):
        for word in sentence.split(' '):
            yield word


def main(stop):
    for word in itertools.islice(extract_word(), stop):
        print(word)


if __name__ == '__main__':
    main(10)

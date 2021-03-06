#記事のカテゴリ名を（行単位ではなく名前で）抽出せよ．

import gzip
import json
import re


def search (filename, keyword):
    with gzip.open( filename,'rt',encoding="utf-8") as opendedfile:
        for line in opendedfile:
            filedict = json.loads(line)

            if (filedict["title"] == keyword):
                return filedict["text"]


filename=r"\Users\Koya\Documents\Lab\jawiki-country.json.gz"

sentence = search(filename, "イギリス").split("\n")

for line in sentence:
    line=re.search(r"Category:(?P<category>.+?)(\||])", line)  ##[[Category:イギリス|*]]
    if line:
        print(line.group("category"))


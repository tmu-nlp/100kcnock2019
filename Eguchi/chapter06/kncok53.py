#Stanford Core NLPを用い，入力テキストの解析結果をXML形式で得よ．
# また，このXMLファイルを読み込み，入力テキストを1行1単語の形式で出力せよ．
from pycorenlp import StanfordCoreNLP
from nltk import stem
import re
import time
import xml.etree.ElementTree as ET

path = r"C:\Users\Koya\Documents\Lab\100knock2019\Eguchi\chapter06\nlp.txt"
path2 = r"C:\Users\Koya\Documents\Lab\100knock2019\Eguchi\chapter06\nlp.txt.xml"
def nlp_make():
        with open(path,mode = "r",encoding='utf-8' ) as f:
                text = f.read()
        
        nlp = StanfordCoreNLP("http://localhost:9000")
        output = nlp.annotate(text, properties={'timeout': '50000',
                'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,dcoref',
                'outputFormat': 'xml'
                })        
        print(len(output))
        with open(path2, 'w') as f:
                f.write(output)

def analyzer():
        tree = ET.parse(path2)
        root = tree.getroot()
        for i , word in enumerate(root.iter("word")):
                if i == 50:
                        break
                print(word.text)
                
#nlp_make()
analyzer()
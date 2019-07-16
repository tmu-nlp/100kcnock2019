#極性分析に有用そうな素性を各自で設計し，学習データから素性を抽出せよ．
#素性としては，レビューからストップワードを除去し，各単語をステミング処理したものが最低限のベースラインとなるであろう．
import collections
import codecs
from nltk import stem

def reg_stop_word():
    stop_words = [
                "i,me,my,myself,we,our,ours,ourselves,you,your,yours",
                "yourself,yourselves,he,him,his,himself,she,her,hers",
                "herself,it,its,itself,they,them,their,theirs,themselves",
                "what,which,who,whom,this,that,these,those,am,is,are,was",
                "were,be,been,being,have,has,had,having,do,does,did",
                "doing,a,an,the,and,but,if,or,because,as,until,while",
                "of,at,by,for,with,about,against,between,into,through",
                "during,before,after,above,below,to,from,up,down,in,out",
                "on,off,over,under,again,further,then,once,here,there",
                "when,where,why,how,all,any,both,each,few,more,most",
                "other,some,such,no,nor,not,only,own,same,so,than,too",
                "very,can,will,just,don,should,now"
            ]
    stop_word_list = []
    for words in stop_words:
        for word in words.split(","):
            stop_word_list.append(word)

    return stop_word_list

def detect(sentence, stop_list):
    sentence = sentence.lower()
    for word in sentence.split():
        return word in stop_list



def extract():
    input_path = r"C:\Users\Koya\Documents\Lab\sentiment.txt"
    
    fencoding = "cp1252"
    label_list = list()
    without_label_list = list()
    line_list = list()
    stemmer = stem.PorterStemmer()

    with codecs.open(input_path, "r", fencoding) as f:
        for line in f:
            label = line[:2]
            without_label = line[3:]
            without_label_list.append(without_label)    
            label_list.append(label)
            for word in without_label.split(" "):
                if detect(word, reg_stop_word()) :
                    continue
                word= stemmer.stem(word)
                line_list.append(word)
    counter = collections.Counter(line_list)
    output = list()
    for line, num  in counter.items():
        if num > 5:        
            output.append(line)
    
    print(output)
extract()
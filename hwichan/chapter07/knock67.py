import json
import pymongo
from pymongo import MongoClient


def main():
    client = MongoClient('localhost', 27017)  # 第一引数にはアドレス、第二引数にはポート番号

    # データベースの呼び出し、なかったら自動的に作成される
    db = client.knock64

    # コレクションの呼び出し、RDBでいうとテーブル、なかったら自動的に作成される
    collection = db.artist_info

    name = input('アーティストの別名を入力してください : ')

    # collection.find({'name':'Queen'}) -> <class 'pymongo.cursor.Cursor'>
    for n, value in enumerate(collection.find({'aliases.name': name}), 1):
        # json.dumps(value, indent=2) はエラー
        # idが特殊な型であるから変換できない、idを削除
        del value["_id"]
        print(f'{n}件目')
        # indent=2 : dictを整形, ensure_ascii=False : これを指定しないと日本語がバイト型で出力される
        print(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()


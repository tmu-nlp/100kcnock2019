'''
60. KVSの構築
Key-Value-Store (KVS) を用い，
アーティスト名（name）から活動場所（area）を検索するためのデータベースを構築せよ．
'''
import sys
import gzip
import json
import leveldb


def message(text):
    sys.stderr.write(f"\33[92m{text}\33[0m\n")


fname = 'artist.json.gz'
db_name = 'name2area'

db = leveldb.LevelDB(db_name)

if sum(1 for _ in db.RangeIter(include_value=False)) == 921337:
    message("[*] skip")
else:
    with gzip.open(fname, 'rt') as f:
        for json_data in map(json.loads, f):
            name = f"{json_data['name']}\t{json_data['id']}"
            area = json_data.get('area', '""')
            db.Put(name.encode(), area.encode())

fname_db_size = sum(1 for _ in db.RangeIter(include_value=False))
message(f'[+] {db_name} のサイズ -> {fname_db_size}')


'''
* LevelDB
    - https://github.com/google/leveldb
    - https://code.google.com/archive/p/py-leveldb/
    - http://blog.livedoor.jp/wolf200x/archives/53052954.html
    cf. plyvel
* LevelDB入門 (基本編)
    - https://yosuke-furukawa.hatenablog.com/entry/2014/05/05/095207
* JSON形式の概要は以下の通りである．
フィールド	           型	内容	例
id	                  ユニーク識別子	整数	20660
gid	                  グローバル識別子	文字列	"ecf9f3a3-35e9-4c58-acaa-e707fba45060"
name	              アーティスト名	文字列	"Oasis"
sort_name	          アーティスト名（辞書順整列用）	文字列	"Oasis"
area	              活動場所	文字列	"United Kingdom"
aliases	              別名	辞書オブジェクトのリスト
aliases[].name	      別名	文字列	"オアシス"
aliases[].sort_name	  別名（整列用）	文字列	"オアシス"
begin	              活動開始日	辞書
begin.year	          活動開始年	整数	1991
begin.month	          活動開始月	整数
begin.date	          活動開始日	整数
end	                  活動終了日	辞書
end.year	          活動終了年	整数	2009
end.month	          活動終了月	整数	8
end.date	          活動終了日	整数	28
tags	              タグ	辞書オブジェクトのリスト
tags[].count	      タグ付けされた回数	整数	1
tags[].value          タグ内容	文字列	"rock"
rating	              レーティング	辞書オブジェクト
rating.count	      レーティングの投票数	整数	13
rating.value	      レーティングの値（平均値）	整数	86
'''

class Morph:
    # コンストラクタ
    # surface(表層形), base(基本形), pos(品詞), pos1(品詞細分類1)
    def __init__(self, surface, base, pos, pos1):
        self.surface = surface
        self.base = base
        self.pos = pos
        self.pos1 = pos1

    # __str__ オブジェクトを文字列にして返す
    def __str__(self):
        return 'surface[{}]\tbase[{}]\tpos[{}]\tpos1[{}]'.format(self.surface, self.base, self.pos, self.pos1)


class Chunk:
    def __init__(self):
        self.morphs = []  # 文節のmorph、1文節ごとのMorphインスタンスが格納
        self.srcs = []  # 係り元文節番号、二個ある場合があるから配列
        self.dst = -1  # 係り先文節番号

    def __str__(self):
        surface = ''
        for morph in self.morphs:
            surface += morph.surface
        return '{}\tsrcs{}\tdst[{}]'.format(surface, self.srcs, self.dst)

    def return_surface(self):
        surface = ''
        for morph in self.morphs:
            if morph.pos != '記号':  # 句読点は出力しない
                surface += morph.surface
        return surface

    # 最左の動詞ということは一番初めにヒットした動詞？
    def check_verb(self):
        for morph in self.morphs:
            if morph.pos == "動詞":
                return morph

    # 助詞が複数ある場合は一つのみ選択し格助詞を優先、または最後の助詞を選択
    # くるにも 31456
    # 及ばんさと 31460
    def check_josi(self):
        josi_list = []

        for morph in self.morphs:
            if morph.pos1 == "格助詞":
                return morph
            elif morph.pos == "助詞":
                josi_list.append(morph)

        if josi_list:
            return josi_list[len(josi_list) - 1]


def read_file(filename: str) -> str:
    c_list = []
    with open(filename, 'r') as f:
        for line in f:
            tree = c.parse(line)
            c_list.append(tree.toString(CaboCha.FORMAT_LATTICE))

    return ''.join(c_list)


def write_file(text: str, filename: str):
    with open(filename, 'w') as f:
        f.write(text)


def make_list(filename: str):
    with open(filename, 'r') as f:
        chunks = dict()  # idxをkeyにして,keyごとにChunkインスタンスを格納
        idx = -1  # 文節番号
        for line in f:
            if line == 'EOS\n':  # 1文の終了, chunksをyieldで返す
                if len(chunks) > 0:  # EOS\tが連続するとこがあるから

                    sorted_tuple = sorted(chunks.items(), key=lambda x: x[0])  # key(文節番号)でソート
                    yield list(zip(*sorted_tuple))[1]  # value('{}\tsrcs{}\tdst[{}]')のみ返す
                    chunks.clear()

                else:
                    yield []

            elif line[0] == '*':  # 最初の文字が'*'の場合、係り受け解析結果
                # * 0 2D 0/0 -0.764522
                line = line.split(' ')
                idx = int(line[1])  # 文節番号、0
                # 2D
                dst = int(line[2][:-1])  # 係り先番号、2

                # 下の処理(係り元番号のセット)をするときもChunkインスタンスを生成するためkeyがかぶってないか確認
                if idx not in chunks:  # 文節番号のキーがなかったらChunkを生成
                    chunks[idx] = Chunk()
                chunks[idx].dst = dst  # 係り先番号をセット(dst)

                # 係り元番号のセット(srcs)、係り先番号のChunkに現在の文節番号をsrcsにセット
                if dst != -1:  # dst = -1は係り先がない
                    if dst not in chunks:
                        chunks[dst] = Chunk()
                    # 係り先の文節では現在の文節が係り元
                    chunks[dst].srcs.append(idx)

            else:
                # 吾輩	名詞,代名詞,一般,*,*,*,吾輩,ワガハイ,ワガハイ,,
                line = line.split('\t')
                cal1 = line[0]
                cal2 = line[1].split(',')
                chunks[idx].morphs.append(Morph(cal1, cal2[6], cal2[0], cal2[1]))


def main():
    p_list = []
    for i, chunks in enumerate(make_list('neko.txt.cabocha')):
        if i == 7:
            for j, chunk in enumerate(chunks):
                morph = chunk.check_verb()  # morph : 文節の動詞のMorphクラスのインスタンス
                srcs = chunk.srcs  # 係り元番号
                josi_list = []  # 助詞のみを格納
                josi_surface = []  # 助詞がある文節(係り元)を格納
                if morph and srcs:
                    for s in srcs:  # srcsはlistなので
                        josi = chunks[s].check_josi()  # 係り元に助詞があるかをチェック, chunks[s] : 係り元の文節, Chunkクラス
                        if josi:
                            josi_list.append(josi.base)
                            # 係り元のChunkインスタンスのreturn_surface関数を使い文節を取り出す
                            josi_surface.append(chunks[s].return_surface())

                if josi_list:
                    josi_list = sorted(josi_list)
                    p_list.append('{}\t{}\t{}'.format(morph.base, '\t'.join(josi_list), '\t'.join(josi_surface)))
            break

    print('\n'.join(p_list))
    # text = '\n'.join(p_list)
    # write_file(text, 'knock46.txt')


if __name__ == "__main__":
    main()


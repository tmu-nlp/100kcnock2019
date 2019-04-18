'''
02. 「パトカー」＋「タクシー」＝「パタトクカシーー」
「パトカー」＋「タクシー」の文字を先頭から交互に連結して文字列「パタトクカシーー」を得よ．
'''


def knock02(s1: str, s2: str) -> str:
    return ''.join(c1 + c2 for c1, c2 in zip(s1, s2))


if __name__ == '__main__':
    print(knock02("パトカー", "タクシー"))  # パタトクカシーー
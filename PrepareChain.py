import unittest
import re
import MeCab
import sqlite3
from collections import defaultdict



#チェーンを作成してdbに保存するクラス
class PrepareChain(object):

    BEGIN = u"__BEGIN_SENTENCE__"
    END = u"__END_SENTENCE__"

    DB_PATH = "chain.db"
    DB_SCHEMA_PATH = "schema.sql"


    #初期メソッド
    def __init__(self, text):
        self.text = text

         #形態素解析用タガー
        self.tagger = MeCab.Tagger('-d /opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd -Ochasen')
    

    #形態素解析から３つ組の出現回数まで
    def make_triplet_freqs(self):

        #長い文章をセンテンス毎に分割
        sentences = self._divide(self.text)

        #３つ組の出現回数
        triplet_freqs = defaultdict(int)

        #センテンス毎に３つ組にする
        for sentence in sentences:
            #形態素解析
            morphemes = self._morphological_analysis(sentence)
            #３つ組をつくる
            triplets = self._make_triplet(morphemes)
            #出現回数を加算
            for (triplet, n) in triplets.items():
                triplet_freqs[triplet] += n

        return triplet_freqs


    #区切られた長い文章を一文ずつに分ける
    def _divide(self, text):

        #改行文字以外の分割文字
        delimiter = u"。|．|\."

        #全ての分割文字を改行文字に置換
        text = re.sub(r"({})".format(delimiter), r"\1\n", text)

        #改行文字で分割
        sentences = text.splitlines()

        #前後の空白文字を削除
        sentences = [sentence.strip() for sentence in sentences]

        return sentences
    

    #一文を形態素解析する
    def _morphological_analysis(self, sentence):
        morphemes = []
        node = self.tagger.parseToNode(sentence)
        while node:
            if node.posid != 0:
                morpheme = node.surface
                morphemes.append(morpheme)
            node = node.next
        return morphemes
    

    #形態素解析で分割された配列を、形態そ毎に３つ組にしてその出現回数を数える
    def _make_triplet(self, morphemes):

        #3つ組をつくれない場合は終える
        if len(morphemes) < 3:
            return {}
        
        #出現回数の辞書
        triplet_freqs = defaultdict(int)

        #繰り返し
        for i in range(len(morphemes) - 2):
            triplet = tuple(morphemes[i:i + 3])
            triplet_freqs[triplet] += 1
        
        #beginを追加
        triplet = (PrepareChain.BEGIN, morphemes[0], morphemes[1])
        triplet_freqs[triplet] = 1

        #endを追加
        triplet = (morphemes[-2], morphemes[-1], PrepareChain.END)
        triplet_freqs[triplet] = 1

        return triplet_freqs


    #３つ組毎に出現回数をDBに保存
    def save(self, triplet_freqs, init=False):

        #DBオープン
        con = sqlite3.connect(PrepareChain.DB_PATH)

        #初期化からの場合
        if init:
            with open(PrepareChain.DB_SCHEMA_PATH, "r") as f:
                schema = f.read()
                con.executescript(schema)
            
            datas = [(triplet[0], triplet[1], triplet[2], freq)
            for (triplet, freq) in triplet_freqs.items()]

            p_statement = u"insert into chain_freqs (prefix1, prefix2, suffix, freq) values (?, ?, ?, ?)"
            con.executemany(p_statement, datas)
        
        #コミットしてクローズ
        con.commit()
        con.close()
    

    #３つ組毎の出現回数を出力する
    def show(self, triplet_freqs):
        for triplet in triplet_freqs:
            print("|".join(triplet), "\t", triplet_freqs[triplet])



if __name__ == "__main__":
    f = open("data.txt", encoding="utf-8")
    text = f.read()
    f.close()
    chain = PrepareChain(text)
    triplet_freqs = chain.make_triplet_freqs()
    chain.save(triplet_freqs, True)





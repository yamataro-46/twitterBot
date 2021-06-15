import os
import re
import requests
import tweepy
import json

file = open('info.json', 'r')
info = json.load(file)

# APIの秘密鍵(実際のプログラムでは環境変数を使っています)
CONSUMER_KEY = info['CONSUMER_KEY']
CONSUMER_SECRET = info['CONSUMER_SECRET']
ACCESS_TOKEN_KEY = info['ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = info['ACCESS_TOKEN_SECRET']


def gettweet(CK, CKS, AT, ATS):

    # APIに接続
    auth = tweepy.OAuthHandler(CK, CKS)
    auth.set_access_token(AT, ATS)
    api = tweepy.API(auth)

    # ユーザを指定してRTを除いたツイートを取得
    name="@yamath_314"
    results=api.user_timeline(screen_name=name,count=50,include_rts=False)

    f=open(r"/Users/ryodai/Documents/MyPython/twitter_bot/data.txt",mode="a",encoding="utf-8")

    for result in results:

        #リンクの削除
        result.text=re.sub(r"https?://[\w/:%#\$&\?\(\)~\.=\+\-…_]+", "" ,result.text)

        #@ツイートの削除(昔仲良くしていたけど今ブロ解された…みたいな人に行くと地獄なので)
        result.text=re.sub("@[\w]+","",result.text)

        #「#peing」「#質問箱」を消す
        result.text=re.sub("#peing","",result.text)
        result.text=re.sub("#質問箱","",result.text)

        #data.txtに追加で書き込み
        f.write(result.text+"\n")

    f.close()

if __name__=="__main__":
    gettweet(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN_KEY,ACCESS_TOKEN_SECRET)
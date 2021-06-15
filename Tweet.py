from requests_oauthlib import OAuth1Session
import json
import schedule
import time
from GenerateText import GenerateText
import json

file = open('info.json', 'r')
info = json.load(file)

# APIの秘密鍵(実際のプログラムでは環境変数を使っ
CONSUMER_KEY = info['CONSUMER_KEY']
CONSUMER_SECRET = info['CONSUMER_SECRET']
ACCESS_TOKEN_KEY = info['ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = info['ACCESS_TOKEN_SECRET']

    # APIに接続
twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

def job():
    #ツイート
    tweet = GenerateText().generate()
    params = {"status": tweet}
    req = twitter.post("https://api.twitter.com/1.1/statuses/update.json", params = params)


    f=open(r"/Users/ryodai/Documents/MyPython/twitter_bot/data.txt",mode="a",encoding="utf-8")
    #data.txtに追加で書き込み
    f.write(tweet+"\n")
    f.close()


def main():
    schedule.every().day.at("12:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()


""" if req.status_code == 200:
    print("succeed" + "/" + tweet)
else:
    print("Error: %d" % req.status_code) """
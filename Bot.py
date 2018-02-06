import requests
import simplejson as json
import tweepy
import time


# Verilen json text'inden atilacak twiti olustur
def createTweet(text):
    info = json.loads(text)
    string = ""
    for item in info:
        string += "#{} ${:.6} {:>6}%\n" \
            .format(item['symbol'], item['price_usd'], item['percent_change_24h'])
        # tweet.append(string)
    return string


# Json dosyasindan twitter access token bilgilerini al
with open("TwitterApiKeys.json") as file:
    twitterKeys = json.load(file)
    file.close()

# Tweepy modulunu ayarla
oauth = tweepy.OAuthHandler(twitterKeys['consumer_key'], twitterKeys['consumer_secret'])
oauth.set_access_token(twitterKeys['access_token'], twitterKeys['access_token_secret'])
api = tweepy.API(oauth)

# CoinMarketCap.com Api
# Api'den gelen sonuclari her 2 saatte bir tweet at
while True:
    params = {"limit": "10"}
    r = requests.get("https://api.coinmarketcap.com/v1/ticker/", params=params)
    tweet = createTweet(r.text)
    print(tweet)
    api.update_status(tweet)
    time.sleep(60 * 60 * 2)  # Sleep for 2 hours

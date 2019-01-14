from bs4 import BeautifulSoup
import requests
import tweepy
import config


def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])

    return tweepy.API(auth)


PAGE_LINK = 'https://weather.com/en-IN/weather/today/l/EGXX0001:1:EG'


def main():
    page = requests.get(PAGE_LINK)
    page_response = requests.get(PAGE_LINK, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    LOCATION = page_content.find(
        class_='h4 today_nowcard-location').text.encode('utf-8').strip()
    DEGREE = page_content.find(
        class_="today_nowcard-temp").text.encode('utf-8').strip()
    TODAY_PHRASE = page_content.find(
        class_="today_nowcard-phrase").text.encode('utf-8').strip()
    FEELS = page_content.find(
        class_="today_nowcard-feels").text.encode('utf-8').strip()
    asof = page_content.find(
        class_="today_nowcard-timestamp").text.encode('utf-8').strip()
    full = '#Alexandria ' + asof + ' ' + TODAY_PHRASE + ' ' + \
        DEGREE + ' and ' + FEELS + ' #weather'
    # Fill in the values noted in previous step here
    cfg = {
        "consumer_key": config.twitter['consumerkey'],
        "consumer_secret": config.twitter['consumersecret'],
        "access_token": config.twitter['accesstoken'],
        "access_token_secret": config.twitter['accesstokensecret']
    }

    api = get_api(cfg)
    tweet = full
    status = api.update_status(status=tweet)


if __name__ == '__main__':
    main()

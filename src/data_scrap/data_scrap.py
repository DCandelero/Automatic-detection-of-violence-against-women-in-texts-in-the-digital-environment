import os
import sys
import tweepy
import requests
from dotenv import load_dotenv

sys.path.append('../../')
import config

load_dotenv(os.path.join(config.PROJ_PATH, '.env')) 

def set_twitter_access():
    consumer_key = os.environ["API_KEY"]
    consumer_secret = os.environ["API_KEY_SECRET"]
    access_token = os.environ["ACCESS_TOKEN"]
    access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

    auth = tweepy.OAuth1UserHandler(
        consumer_key, 
        consumer_secret, 
        access_token, 
        access_token_secret
    )

    api = tweepy.API(auth)

    return api

def save_tweet_text(tweet:object, text_type='') -> None:
    tweet_timestamp = str(tweet.created_at.strftime("%Y-%m-%d %H-%M-%S"))
    tweet_id = str(tweet.id)
    txt_file_name = os.path.join(config.DATA_PATH_RAW_TEXTS, '{}_{}.txt'.format(tweet_timestamp, tweet_id))
    
    with open(txt_file_name, 'w', encoding="utf-8") as txt_file:
        try:
            if text_type == 'retweet':
                txt_file.write(tweet.retweeted_status.full_text)
            else:
                txt_file.write(tweet.full_text)
            # txt_file.write(tweet.retweeted_status.full_text)
        except AttributeError:
            print('Unable to read text from tweet {}'.format(tweet.id))
            print("=====")

    return None

def DownloadFile(url:str, path_to_save:str) -> None:
    response = requests.get(url)

    if response.status_code == 200:
        with open(path_to_save, 'wb') as f:
                f.write(response.content)
    return None


def save_tweet_image(tweet:object) -> None:
    tweet_timestamp = str(tweet.created_at.strftime("%Y-%m-%d %H-%M-%S"))
    tweet_id = str(tweet.id)

    try:
        for media in tweet.entities.get("media",[{}]):
            #checks if there is any media-entity
            if media.get("type",None) == "photo":
                tweet_media_id = str(media['id'])
                filename = os.path.join(config.DATA_PATH_RAW_IMAGES, '{}_{}_{}.png'.format(tweet_timestamp, tweet_id, tweet_media_id))
                DownloadFile(media["media_url"], filename)
    except AttributeError:
        print('Unable to read medias from tweet {}'.format(tweet_id))
        print("=====")

def extract_tweets(extract_keyword:str):
    api = set_twitter_access()
    
    tweets_pages = []
    for status in tweepy.Cursor(api.search_tweets,
                                extract_keyword, 
                                tweet_mode='extended', 
                                lang='pt', 
                                count=2).pages(3):
        tweets_pages.append(status)

    # Read tweets
    for page in tweets_pages:
        for tweet in page:
            save_tweet_text(tweet)
            print(tweet.full_text)

            save_tweet_image(tweet)

            if tweet.coordinates is not None:
                print(tweet.coordinates)
                print(tweet.geo)
                print(tweet.contributors)
                break


def get_extracted_text():
    extracted_text_list = os.listdir(config.DATA_PATH_RAW_TEXTS)

    if extracted_text_list:
        fname = os.path.join(config.DATA_PATH_RAW_TEXTS, extracted_text_list[0])

        extracted_text = ''
        with open(fname, 'r', encoding="utf8") as text_file:
            extracted_text = text_file.read()

        return extracted_text
    else:
        return 'Extraia mais textos'
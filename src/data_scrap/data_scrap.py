import os
import sys
import tweepy
import requests
import pandas as pd
from dotenv import load_dotenv
import pickle

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

def save_tweets_information(tweets:list, keywords_to_extract:list=None, save_tweet:bool=True):
    tweet_columns = ['id', 'text', 'lang', 'keywords_extraction','created_at','user_id','user_name','user_screen_name','user_profile_image_url',
                                 'user_created_at','place_id','place_type','place_name','country','country_code','coordinates']
    tweet_df = pd.DataFrame(columns=tweet_columns)
    for tweet in tweets:
        tweet_data = {'id': tweet.id, 'text': tweet.full_text, 'lang': tweet.lang,'keywords_extraction': keywords_to_extract,
                      'created_at': tweet.created_at, 'user_id': tweet.user.id_str, 'user_name': tweet.user.name, 
                      'user_screen_name': tweet.user.screen_name, 'user_profile_image_url': tweet.user.profile_image_url, 
                      'user_created_at': tweet.user.created_at, 'place_id': getattr(tweet.place, 'id', None), 
                      'place_type': getattr(tweet.place, 'place_type', None), 
                      'place_name': getattr(tweet.place,'name', None), 'country': getattr(tweet.place,'country', None), 
                      'country_code': getattr(tweet.place,'country_code', None), 
                      'coordinates': getattr(getattr(tweet.place,'bounding_box', None), 'coordinates', None)}
        tweet_df = tweet_df.append(tweet_data, ignore_index = True)

        # Save tweet
        if save_tweet:
            fname = os.path.join(config.DATA_PATH_RAW_TWEETS, str(tweet.id)+'.pkl')
            with open(fname, 'wb') as file:
                pickle.dump(tweet, file)
                print(f'Object successfully saved to "{fname}"')
    
    extracted_tweets_path = os.path.join(config.DATA_PATH_WRANGLE_TWEETS, 'extracted_tweets.parquet')
    if os.path.exists(extracted_tweets_path):
        tweet_df.to_parquet(extracted_tweets_path, engine='fastparquet', append=True)
    else:
        tweet_df.to_parquet(extracted_tweets_path, engine='fastparquet')
    
    last_extraction_tweets_path = os.path.join(config.DATA_PATH_WRANGLE_TWEETS, 'last_extraction_tweets.parquet')
    tweet_df.to_parquet(last_extraction_tweets_path)


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

def extract_tweets(to_extract, place:str=''):
    api = set_twitter_access()

    query = ""
    if place:
        query += f'place:{place} AND '

    if type(to_extract) is list:
        keywords_query = ' OR '.join(to_extract)
        query += f'({keywords_query})'
    else:
        query += to_extract
    
    tweets_pages = []
    for status in tweepy.Cursor(api.search_tweets,
                                query, 
                                tweet_mode='extended', 
                                lang='pt', 
                                count=1).pages(5):
        tweets_pages.append(status)

    # Read tweets
    tweets = []
    for page in tweets_pages:
        for tweet in page:
            tweets.append(tweet)
            save_tweet_text(tweet)
            save_tweet_image(tweet)

            if tweet.coordinates is not None:
                print(tweet.coordinates)
                print(tweet.geo)
                print(tweet.contributors)
                break
    save_tweets_information(tweets, to_extract)


def get_extracted_text(folder_path:str):
    extracted_text_list = os.listdir(folder_path)

    if extracted_text_list:
        fname = os.path.join(folder_path, extracted_text_list[0])

        extracted_text = ''
        with open(fname, 'r', encoding="utf8") as text_file:
            extracted_text = text_file.read()

        return extracted_text, fname
    else:
        return 'Extraia mais textos', ''

def delete_extracted_text(folder_path:str):
    extracted_text_list = os.listdir(folder_path)

    if extracted_text_list:
        fname = os.path.join(folder_path, extracted_text_list[0])

        os.remove(fname)

def save_extracted_text(data_str:str, folder_path:str, file_name:str):
    fname = os.path.join(folder_path, file_name)

    with open(fname, 'w', encoding="utf8") as text_file:
        text_file.write(data_str)
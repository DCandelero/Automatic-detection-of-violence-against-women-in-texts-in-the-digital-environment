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

def save_tweets_information(tweets:tweepy.client.Response, search_keywords:list=None):
    # Get users informations from tweets
    users = {u["id"]: u for u in tweets.includes['users']}
    # Get places informations from tweets, if exists
    try:
        places = {p["id"]: p for p in tweets.includes['places']}
    except KeyError:
        print("Tweets extraídos não tem componente de localização.")

    # Create dataframe with tweet info
    tweet_columns = ['id', 'text', 'lang', 'keywords_extraction','created_at','user_id','user_name','user_screen_name','user_profile_image_url',
                                    'user_created_at','place_id','place_type','place_name','country','country_code','coordinates']
    tweet_df = pd.DataFrame(columns=tweet_columns)

    for tweet in tweets.data:
        tweet_data = {}
        extracted_keywords = [keyword for keyword in search_keywords if keyword.lower() in tweet.text.lower()]
        tweet_data['keywords_extraction'] = extracted_keywords
        tweet_data['id'] = int(tweet.id)
        tweet_data['text'] = tweet.text
        tweet_data['lang'] = tweet.lang
        tweet_data['created_at'] = tweet.created_at
        if users[tweet.author_id]:
            user = users[tweet.author_id]
            tweet_data['user_id'] = int(user.id)
            tweet_data['user_name'] = user.name
            tweet_data['user_screen_name'] = user.username
            tweet_data['user_profile_image_url'] = user.profile_image_url
            tweet_data['user_created_at'] = user.created_at
        try:
            place = places[tweet.geo['place_id']]
            tweet_data['place_id'] = int(place.id)
            tweet_data['country'] = place.country
            tweet_data['country_code'] = place.country_code
            tweet_data['place_type'] = place.place_type
            tweet_data['place_name'] = place.name
            tweet_data['coordinates'] = place.geo['bbox']

        except:
            pass

        # Save tweet
        fname = os.path.join(config.DATA_PATH_RAW_TWEETS_V2, str(tweet.id)+'.pkl')
        with open(fname, 'wb') as file:
            pickle.dump(tweet_data, file)
            print(f'Object successfully saved to "{fname}"')

        tweet_df = tweet_df.append(tweet_data, ignore_index = True)
    
    extracted_tweets_path = os.path.join(config.DATA_PATH_WRANGLE_TWEETS, 'extracted_tweets.parquet')
    if os.path.exists(extracted_tweets_path):
        tweet_df.to_parquet(extracted_tweets_path, engine='fastparquet', append=True)
    else:
        tweet_df.to_parquet(extracted_tweets_path, engine='fastparquet')
    
    last_extraction_tweets_path = os.path.join(config.DATA_PATH_WRANGLE_TWEETS, 'last_extraction_tweets.parquet')
    tweet_df.to_parquet(last_extraction_tweets_path)

def make_query(search_keywords:list, complementary_words:list=[]):
    places = config.PLACES
    lang = config.LANG

    query = ''

    if len(search_keywords) > 0:
        keywords_query = ''
        for idx, keyword in enumerate(search_keywords):
            if idx == 0:
                keywords_query += '('
            if idx == len(search_keywords) - 1:
                keywords_query += f'"{keyword}")'
                break
            keywords_query += f'"{keyword}" OR '
        query += f'{keywords_query} '

    if len(complementary_words) > 0:
        comp_words_query = ''
        for idx, word in enumerate(complementary_words):
            if idx == 0:
                comp_words_query += '('
            if idx == len(complementary_words) - 1:
                comp_words_query += f'"{word}")'
                break
            comp_words_query += f'"{word}" '
        query += f'{comp_words_query} '

    if len(places) > 0:
        places_query = ''
        for idx, place in enumerate(places):
            if idx == 0:
                places_query += '('
            if idx == len(places) - 1:
                places_query += f'place:"{place}")'
                break
            places_query += f'place:"{place}" '
        query += f'{places_query} '

    query += f'lang:{lang} -is:retweet'

    return query

def extract_tweets(search_keywords:list, complementary_words:list=[], max_results:int=10, info_to_save:str='All'):
    # Setup connection with twitter api_v2
    client = tweepy.Client(bearer_token=os.environ["BEARER_TOKEN"])

    query = make_query(search_keywords, complementary_words)

    tweets = client.search_recent_tweets(query=query, 
                                     tweet_fields=['id', 'text', 'author_id', 'geo', 'lang','created_at'], 
                                     user_fields=['id', 'name', 'username', 'profile_image_url','created_at'], 
                                     place_fields=['id', 'country', 'country_code', 'place_type', 'name', 'geo'],
                                     expansions=['author_id', 'geo.place_id'],
                                     max_results=max_results)

    if info_to_save in ['Tweet', 'All']:
        save_tweets_information(tweets, search_keywords)


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
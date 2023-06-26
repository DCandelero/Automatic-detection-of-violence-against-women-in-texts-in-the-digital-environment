import os
import random
import pandas as pd

import sys
sys.path.append('../../')
import config


def get_extracted_text(folder_path:str):
    extracted_text_list = os.listdir(folder_path)

    if extracted_text_list:
        filename = extracted_text_list[0]
        file_full_path = os.path.join(folder_path, filename)

        extracted_text = ''
        with open(file_full_path, 'r', encoding="utf8") as text_file:
            extracted_text = text_file.read()

        return extracted_text, filename
    else:
        return 'Extraia mais textos', ''
    
def get_extracted_tweets(file_path:str):
    if os.path.exists(file_path):
        last_extracted_tweets = pd.read_parquet(file_path)
        n_of_extracted_tweets = len(last_extracted_tweets)
        if  n_of_extracted_tweets > 0:
            tweet = last_extracted_tweets.iloc[0].to_dict()

            return tweet, n_of_extracted_tweets
    
    return {'text': 'Extraia mais textos'}, 0

def delete_extracted_tweet(file_path:str):
    if os.path.exists(file_path):
        last_extracted_tweets = pd.read_parquet(file_path)
        if  len(last_extracted_tweets) > 0:
            last_extracted_tweets = last_extracted_tweets.drop(0).reset_index(drop=True)
            last_extracted_tweets.to_parquet(file_path)

def save_extracted_tweet(tweet:dict, file_path:str):
    tweet['keywords_extraction'] = list(tweet['keywords_extraction'])
    tweet_df = pd.DataFrame([tweet])
    if os.path.exists(file_path):
        tweet_df.to_parquet(file_path, engine='fastparquet', append=True)
    else:
        tweet_df.to_parquet(file_path, engine='fastparquet')


def delete_extracted_text(folder_path:str):
    extracted_text_list = os.listdir(folder_path)

    if extracted_text_list:
        filename = extracted_text_list[0]
        file_full_path = os.path.join(folder_path, filename)

        os.remove(file_full_path)
        

def save_extracted_text(data_str:str, folder_path:str, file_name:str):
    file_full_path = os.path.join(folder_path, file_name)

    with open(file_full_path, 'w', encoding="utf8") as text_file:
        text_file.write(data_str)

def get_test_or_train_path(train_path:str, test_path:str, percentage_for_test:int=30):
    if random.randint(1,100) <= percentage_for_test:
        return test_path
    else:
        return train_path
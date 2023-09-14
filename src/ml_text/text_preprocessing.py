# General modules
import pandas as pd
import re
import emoji
import unidecode
import string

# Preprocessing modules
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
# nltk.download('punkt')
# from sklearn.feature_extraction.text import CountVectorizer
# from nltk.stem.rslp import RSLPStemmer
# nltk.download('rslp')
# from spellchecker import SpellChecker

def spellCorrection(tokens):
    spell = SpellChecker(language="pt")
    return [spell.correction(token) for token in tokens]

def dropLinks(text):
    text = re.sub(r"http\S+", "", text)
    return text

def tokenize(text):
    words = nltk.word_tokenize(text)
    tokens = [word for word in words if word.isalnum()]
    return tokens

def removeStopwords(text, stop_words_list:list=[]):
    stop_words = set(stopwords.words('portuguese') + stop_words_list)
    text = str(' '.join([word for word in text.split() if word not in stop_words]))
    return text

def abbreviationsReplace(text, abbrv_dict:dict={}):
    if not abbrv_dict:
        abbrv_dict = {"vc": "você",
                "bjs": "beijos",
                "blz": "beleza",
                "pq": "porque",
                " q ": " que ",
                " c ": " com ",
                " p ": " pra "
                }

    for i, j in abbrv_dict.items():
        text = text.replace(i, j)

    return text

def stemming(text):
    lemmatizer = RSLPStemmer()
    words = text.split(" ")
    stemmed_text = ""
    try:
        for word in words:
            stem = lemmatizer.stem(word)
            stemmed_text += stem + " "
    except:
        print(stemmed_text)

    return stemmed_text

def remove_mentions(text:str, start_symbol:str='@'):
    keep_words = []
    for word in text.split(' '):
        if not word.startswith(start_symbol):
            keep_words.append(word)
    return ' '.join(keep_words)


def transform_text(text:str, mode:str='lower'):
    if mode == 'lower':
        return text.lower()

def deaccent_text(text:str):
    return unidecode.unidecode(text)

def remove_digits(text:str):
    return re.sub(r"\d+", "", text)

def remove_special_chars(text:str, chars_list:list=[]):
    if not chars_list:
        chars_list = ' '.join(string.punctuation).split(' ')
    return re.sub(r'[^\w\s]', "", text)

def remove_line_breakers(text:str):
    return text.replace("\n", " ")

def remove_emojis(text:str):
    return emoji.demojize(text,delimiters=("", ""),language='pt')

def remove_repetitions(text:str):
    pattern = re.compile(r"(.)\1{2,}", re.DOTALL)
    return re.sub(pattern, r"\1", text)

def remove_small_texts(text:str, min_length:int=1):
    # tokenize, remove words smaleler than min_length, join text with ' '
    word_tokens = text.split(' ')
    new_word_tokens = []
    for word in word_tokens:
        if len(word) >= min_length:
            new_word_tokens.append(word)
    return ' '.join(new_word_tokens)


def text_preprocessing(text):
    text = remove_mentions(text, '@')
    text = dropLinks(text)
    text = transform_text(text, mode='lower')
    text = removeStopwords(text)
    text = deaccent_text(text)
    text = remove_digits(text)
    text = remove_special_chars(text)
    text = remove_emojis(text)
    text = remove_repetitions(text)
    text = abbreviationsReplace(text)
    text = remove_small_texts(text, 3)
    text = removeStopwords(text)

    return text

def preprocessing(dataframe):
    dataframe.dropna(axis=0, inplace=True)
    dataframe["Text"] = dataframe["Text"].apply(dropLinks)
    dataframe["Text"] = dataframe["Text"].apply(removeStopwords)
    dataframe["Text"] = dataframe["Text"].apply(stemming)
    # dataframe = keyboard_augmentation(dataframe)
    dataframe["Text"] = dataframe["Text"].apply(text_preprocessing)

    return dataframe
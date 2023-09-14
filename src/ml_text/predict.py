import os
import sys
sys.path.append(os.path.join(os.path.join(os.path.dirname(__file__), '..'), '..'))
import config

import text_preprocessing as tp
import pickle

def predict_text(text:str):
    # load model
    model_name = os.path.join(config.DATA_PATH_MODELS, 'v0_model.pkl')
    with open(model_name, 'rb') as file:
        clf = pickle.load(file)
    # load vectorizer
    vectorizer_name = os.path.join(config.DATA_PATH_MODELS, 'v0_vectorizer.pk')
    with open(vectorizer_name, 'rb') as file:
        vectorizer = pickle.load(file)

    text = tp.text_preprocessing(text)
    text = vectorizer.fit_transform([text]).toarray()
    prediction = clf.predict(text)

    return prediction[0]
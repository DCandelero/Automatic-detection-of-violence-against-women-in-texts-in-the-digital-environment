import os
import sys
sys.path.append(os.path.join(os.path.join(os.path.dirname(__file__), '..'), '..'))
import config
from openai_api import get_embedding

import text_preprocessing as tp
import pickle

def predict_text(text:str):
    model_path = os.path.join(config.DATA_PATH_MODELS, 'best.pkl')
    with open(model_path, 'rb') as file:
        loaded_model = pickle.load(file)

    text_embeddings = get_embedding(text)

    prediction = loaded_model.predict([text_embeddings])

    return prediction[0]
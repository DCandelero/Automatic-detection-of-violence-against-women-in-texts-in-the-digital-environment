import openai
import sys
import os
sys.path.append('../../')
import config
from dotenv import load_dotenv

load_dotenv(os.path.join(config.PROJ_PATH, '.env')) 
openai.api_key = os.environ["OPENAI_API_KEY"]

def get_embedding(text, model="text-embedding-ada-002"):
    return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']


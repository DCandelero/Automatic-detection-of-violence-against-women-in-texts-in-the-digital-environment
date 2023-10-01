from pathlib import Path

PROJ_PATH = Path(r'C:\Users\DCandelero\Documents\MBA - USP(Data Analytics)\MBA_TCC')

OFENSIVE_WORDS = ["Amante", "Arregona", "Atirada", "Baranga", "Bruxa", "Burra", "Cadela", "Chifruda",
                  "Chora", "Covarde", "Desastrada", "Desorganizada", "Doida", "Egoista", "Esquisita", 
                  "Estupida", "Falsa", "Farsante", "Feminazi", "Fraca", "Gorda", "Hipocrita", "Histerica", 
                  "Idiota", "Incapaz", "Interesseira", "Jumenta", "Lacraia", "Lerda", "Louca", 
                  "Manipuladora", "Mentirosa", "Merda", "Mocreia", 
                  "Nojenta", "Oferecida", "Passada", "Peppa Pig", "Piranha", "Piriguete", "Porca", "Preguiçosa", 
                  "Promiscua", "Puta", "Ridicula", "Rodada", "Vaca" ,"Vadia", "Vagabunda", 
                  "Velha", "Vergonha"]

DEPRECIATING_PHRASES = ['Você não é capaz', 'Tinha que ser mulher', 
                        'Deve estar saindo com o chefe',' Fecha as pernas', 
                        'Cuidado com o que fala', 'Vai cozinhar', 'Vai lavar louça', 
                        'Deve ser TPM', 'Ser mulher é fácil', 'Lugar de mulher é', 
                        'A culpa é sua', 'Ela tava pedindo', 'Mal comida', 'Vira homem', 
                        'Mal amada', "Mulher de malandro"]
COMPLEMENTARY_SEARCH_WORDS = ['a', 'mulher', 'sua', 'toda']

# Query parameters
LANG = "pt"
PLACES = []
# Brazil, "Portugal", "Mozambique", "Macao", "Luxembourg", "France", "Angola"
COUNTRY_PLACES = ["BR", "PT", "MZ", "MO", "LU", "FR", "AO"]

# Paths
# Data Paths
DATA_PATH = PROJ_PATH / 'data'
DATA_PATH_RAW = DATA_PATH / 'raw'
DATA_PATH_RAW_TEXTS = DATA_PATH_RAW / 'texts'
DATA_PATH_RAW_IMAGES = DATA_PATH_RAW / 'images'
DATA_PATH_RAW_TWEETS = DATA_PATH_RAW / 'tweets'
DATA_PATH_WRANGLE = DATA_PATH / 'wrangle'
DATA_PATH_WRANGLE_TEXTS = DATA_PATH_WRANGLE / 'texts'
DATA_PATH_WRANGLE_IMAGES = DATA_PATH_WRANGLE / 'images'
DATA_PATH_WRANGLE_TWEETS = DATA_PATH_WRANGLE / 'tweets'
DATA_PATH_MODELS = PROJ_PATH / 'models'

# Dataset Paths
DATASET_PATH = PROJ_PATH / 'dataset'
# Texts
DATASET_TEXTS = DATASET_PATH / 'texts'
DATASET_TEXTS_TRAIN = DATASET_TEXTS / 'train'
DATASET_TEXTS_TEST = DATASET_TEXTS / 'test'
# Images
DATASET_IMAGES = DATASET_PATH / 'images'
DATASET_IMAGES_TRAIN = DATASET_IMAGES / 'train'
DATASET_IMAGES_TEST = DATASET_IMAGES / 'test'
# Tweets
DATASET_TWEETS = DATASET_PATH / 'tweets'
DATASET_TWEETS_TRAIN_FILE = DATASET_TWEETS / 'train.parquet'
DATASET_TWEETS_TEST_FILE = DATASET_TWEETS / 'test.parquet'
DATA_PATH_RAW_TWEETS_V1 = DATA_PATH_RAW / 'tweets_v1'
DATA_PATH_RAW_TWEETS_V2 = DATA_PATH_RAW / 'tweets_v2'
DATASET_TWEETS_VAW = DATASET_PATH / 'vaw_tweets'

# Embeddings
EMBEDDINGS_PATH = PROJ_PATH / 'embeddings'

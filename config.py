from pathlib import Path

PROJ_PATH = Path(r'C:\Users\DCandelero\Documents\MBA - USP(Data Analytics)\MBA_TCC')

OFENSIVE_WORDS = ['Burra', 'Gorda', 'Estúpida', 'Interesseira', 'Esquisita', 
                  'Preguiçosa', 'Puta', 'Manipuladora', 'Lerda', 'Incapaz', 
                  'Atirada', 'Piriguete', 'Vadia', 'Piranha', 'Idiota']
DEPRECIATING_PHRASES = ['Você não é capaz', 'Tinha que ser mulher', 
                        'Deve estar saindo com o chefe',' Fecha as pernas', 
                        'Cuidado com o que fala', 'Vai cozinhar', 'Vai lavar louça', 
                        'Deve ser TPM', 'Ser mulher é fácil', 'Lugar de mulher é', 
                        'A culpa é sua', 'Ela tava pedindo', 'Mal comida', 'Vira homem', 
                        'Mal amada']



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


DATASET_PATH = DATA_PATH = PROJ_PATH / 'dataset'
DATASET_TEXTS = DATASET_PATH / 'texts'
DATASET_TEXTS_TRAIN = DATASET_TEXTS / 'train'
DATASET_TEXTS_TEST = DATASET_TEXTS / 'test'
DATASET_IMAGES = DATASET_PATH / 'images'
DATASET_IMAGES_TRAIN = DATASET_IMAGES / 'train'
DATASET_IMAGES_TEST = DATASET_IMAGES / 'test'
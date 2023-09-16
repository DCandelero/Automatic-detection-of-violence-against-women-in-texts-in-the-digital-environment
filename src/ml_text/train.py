import os
import sys
sys.path.append(os.path.join(os.path.join(os.path.dirname(__file__), '..'), '..'))
import config
import pandas as pd
import pickle
import numpy as np

from sklearn.metrics import confusion_matrix 
from scikitplot.metrics import plot_roc_curve, plot_precision_recall_curve
from utils import save_results

import text_preprocessing as tp
from openai_api import get_embedding
from lazypredict.Supervised import LazyClassifier

from tqdm.notebook import tqdm
tqdm.pandas()

import warnings
warnings.filterwarnings('ignore')


def get_train_test_embeddings(train_df:pd.DataFrame, test_df:pd.DataFrame):
    train_embeddings_filename = os.path.join(config.EMBEDDINGS_PATH, f'train_{len(train_df)}_words.csv')
    if os.path.exists(train_embeddings_filename):
        embeddings_df = pd.read_csv(train_embeddings_filename)
        train_df['ada_embedding'] = embeddings_df["ada_embedding"].apply(eval).apply(np.array)
        train_df = train_df.dropna(axis=0, subset=['ada_embedding','text'])
    else:
        train_df['ada_embedding'] = train_df['text_preprocessed'].progress_apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
        train_df.to_csv(train_embeddings_filename, index=False)
        


    test_embeddings_filename = os.path.join(config.EMBEDDINGS_PATH, f'test_{len(test_df)}_words.csv')
    if os.path.exists(test_embeddings_filename):
        embeddings_df = pd.read_csv(test_embeddings_filename)
        test_df['ada_embedding'] = embeddings_df["ada_embedding"].apply(eval).apply(np.array)
        test_df = test_df.dropna(axis=0, subset=['ada_embedding'])
    else:
        test_df['ada_embedding'] = test_df['text_preprocessed'].progress_apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
        test_df.to_csv(test_embeddings_filename, index=False)

    return train_df, test_df

def train(version:str='0'):
    # Load data
    train_df = pd.read_parquet(config.DATASET_TWEETS_TRAIN_FILE)
    test_df = pd.read_parquet(config.DATASET_TWEETS_TEST_FILE)

    # prepare_data
    train_df = train_df.drop_duplicates(['text'])
    train_df['text_preprocessed'] = train_df['text'].apply(lambda text: tp.text_preprocessing(text))
    test_df = test_df.drop_duplicates(['text'])
    test_df['text_preprocessed'] = test_df['text'].apply(lambda text: tp.text_preprocessing(text))

    # Get embeddings
    train_df, test_df = get_train_test_embeddings(train_df, test_df)

    # prepare model input
    x_train = np.array(train_df['ada_embedding'].tolist())
    y_train = np.array(train_df['label'].tolist())
    x_test = np.array(test_df['ada_embedding'].tolist())
    y_test = np.array(test_df['label'].tolist())

    # create and train models
    clf = LazyClassifier(verbose=False, ignore_warnings=True, custom_metric=None, predictions=True)

    df_models_score, predictions = clf.fit(x_train, x_test, y_train, y_test)
    df_models_score = df_models_score.reset_index()
    models = clf.provide_models(x_train, x_test, y_train, y_test)
    
    # Save top 5 models
    version_folder_path = os.path.join(config.DATA_PATH_MODELS, f'v{version}')
    if not os.path.exists(version_folder_path):
        os.mkdir(version_folder_path)
    
    for i in range(5):
        current_clf = models[df_models_score.loc[i, 'Model']]

        model_path = os.path.join(version_folder_path, f'{df_models_score.loc[i, "Model"]}.pkl')
        with open(model_path, 'wb') as file:
            pickle.dump(current_clf, file)

        # Save best model
        if i == 0:
            best_model_path = os.path.join(config.DATA_PATH_MODELS, 'best.pkl')
            with open(best_model_path, 'wb') as file:
                pickle.dump(current_clf, file)

            # calc metrics
            results = {'true_labels': y_test}
            preds = predictions[df_models_score.loc[i, 'Model']]
            results['predictions'] = preds
            cm = confusion_matrix(y_test, preds) 
            results['cm'] = cm
            try:
                preds_proba = current_clf.predict_proba(x_test)
                results['predictions_probs'] = preds_proba
            except:
                pass

            summary_run = {
                'model_name': df_models_score.loc[i, 'Model'],
                'version': 0,
                'train_size': len(train_df),
                'test_size': len(test_df)
            }
            save_file_folder = os.path.join(config.DATA_PATH_MODELS, 'best')
            save_results(results, save_file_folder, summary_run)


train()
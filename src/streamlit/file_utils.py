import os
import random

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

def get_test_or_train_folder_path(percentage_for_test:int=30):
    if random.randint(1,100) <= percentage_for_test:
        return config.DATASET_TEXTS_TEST
    else:
        return config.DATASET_TEXTS_TRAIN
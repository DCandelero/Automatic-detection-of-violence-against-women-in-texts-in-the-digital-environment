import sys
sys.path.append('../data_scrap')
sys.path.append('../../')
from data_scrap import extract_tweets
import config

import streamlit as st
from file_utils import get_extracted_text, delete_extracted_text, save_extracted_text, get_test_or_train_folder_path

# Streamlit page config
st.set_page_config(page_title='dvaw_annotation', page_icon=':violence')

st.sidebar.header('Extração de texto')
extract_text_option = st.sidebar.radio(
    "Como deseja extrair novos textos?",
    ['Palavras chaves pré definidas', 'Texto plano'],
    index=0,
    help='A extração será feita com base nas palavras chaves utilizadas ou no texto plano digitado')
if extract_text_option == 'Palavras chaves pré definidas':
    extract_keyword = st.sidebar.multiselect(
        label='Selecione uma única palavra chave:',
        options=['burra', 'interesseira'],
        default='interesseira')
elif extract_text_option == 'Texto plano':
    extract_keyword = st.sidebar.text_input(
        label='Selecione uma única palavra chave:',
        placeholder='Ninguém vai acreditar em você')
extract_text = st.sidebar.button('Extrair')
if extract_text:
    extract_tweets(extract_keyword)

# Body (extract_tab) =======================================================================================================
st.title('Análise de texto')
extract_tab, predict_tab = st.tabs(['Extração e anotação', 'Predição e validação'])

# Section 1
extract_tab.header('Extração e anotação')
extract_tab.write('Essa página tem como intuito facilitar a extração e anotação de textos que \
            contenham qualquer tipo de violência contra mulheres.' )
extract_tab.markdown('---')

# Section 2
extracted_agression_phrase, extracted_fname = get_extracted_text(config.DATA_PATH_RAW_TEXTS)
extract_tab.code(extracted_agression_phrase)
text_contain_vaw = extract_tab.radio(
    label='O texto acima possuí algum tipo de violência contra mulheres?',
    options =['Não', 'Somente uma parte', 'Sim'],
    key='extract_tab',
    horizontal=True
)
if text_contain_vaw == 'Não':
    extracted_agression_phrase = ''
elif text_contain_vaw == 'Somente uma parte':
    extracted_agression_phrase = extract_tab.text_input(
        label='Cole aqui a parte em que contém a agressão',
        placeholder='Ninguém vai acreditar em você')

next_text = extract_tab.button('Próximo texto')
if next_text:  
    if extracted_agression_phrase:
        folder_path = get_test_or_train_folder_path(percentage_for_test=30)
        save_extracted_text(extracted_agression_phrase, folder_path, extracted_fname)
    delete_extracted_text(config.DATA_PATH_RAW_TEXTS)
    st.experimental_rerun()
extract_tab.markdown('---')

# Section 3
extract_tab.markdown('*Todos textos que possuirem violência direcionada as mulheres serão utilizadas \
    para treino do algoritmo de machine learning*')
extract_tab.markdown('---')

# Body (predict_tab) =======================================================================================================
# Section 1
predict_tab.header('Predição e validação')
predict_tab.write('Essa página tem como intuito conferir se o algoritmo de machine learning \
            identificou corretamente se houve violência contra mulheres no texto analisado.' )
predict_tab.markdown('---')

# # Section 2
# if not next_text:
#     extracted_agression_phrase, extracted_fname = get_extracted_text(config.DATA_PATH_RAW_TEXTS)
# predict_tab.code(extracted_agression_phrase)
# text_contain_vaw = predict_tab.radio(
#     label='O algoritmo detectou corretamente se houve violência contra mulheres na frase acima?',
#     options =['Não', 'Sim'],
#     key='predict_tab',
#     horizontal=True
# )

# next_text = predict_tab.button('Próximo texto')
# if next_text:  
#     delete_extracted_text(config.DATA_PATH_RAW_TEXTS)
#     extracted_agression_phrase, extracted_fname = get_extracted_text(config.DATA_PATH_RAW_TEXTS)
# predict_tab.markdown('---')

# # Section 3
# predict_tab.write('Todos textos que possuirem violência direcionada as mulheres serão utilizadas \
#     para criação de um dashboard para análise dos casos')
# predict_tab.markdown('---')

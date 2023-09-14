import sys
import os
import webbrowser
sys.path.append('../../')
sys.path.append('../data_scrap')
sys.path.append('../ml_text')
import config
from scrap_twitter_api_v2 import extract_tweets
from predict import predict_text
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import streamlit as st
from file_utils import get_extracted_tweets, save_extracted_tweet, get_test_or_train_path, delete_extracted_tweet

def set_button_to_true(button_name:str):
    st.session_state[button_name] = True

def set_button_to_false(button_name:str):
    st.session_state[button_name] = False

# Streamlit page config
st.set_page_config(page_title='dvaw_annotation', page_icon=':violence')

# Sidebar
st.sidebar.header('Extração de texto')
complementary_words = []
extract_text_option = st.sidebar.radio(
    "Como deseja extrair novos textos?",
    ['Palavras chaves (Predefinidas)', 'Frases (Predefinidas)', 'Digite'],
    index=0,
    help='A extração será feita com base nas palavras chaves, frases ou texto digitado')
if extract_text_option == 'Palavras chaves (Predefinidas)':
    search_keywords = st.sidebar.multiselect(
        label='Selecione palavras chave:',
        options=["Todos"]+config.OFENSIVE_WORDS,
        default=config.OFENSIVE_WORDS[0])
    if "Todos" in search_keywords:
        search_keywords = config.OFENSIVE_WORDS
    complementary_words = st.sidebar.multiselect(
        label='Selecione palavras complementares:',
        options=config.COMPLEMENTARY_SEARCH_WORDS)
elif extract_text_option == 'Frases (Predefinidas)':
    search_keywords = st.sidebar.selectbox(
        label='Selecione uma frase:',
        options=config.DEPRECIATING_PHRASES,
        index=0,)
else:
    search_keywords = st.sidebar.text_input(
        label='Digite uma frase ou palavra chave',
        placeholder='Ninguém vai acreditar em você')
    
extract_text = st.sidebar.button('Extrair')
if extract_text:
    extract_tweets(search_keywords, complementary_words, info_to_save='Tweet')

# Adicionar palavras complementares

# Body (extract_tab) =======================================================================================================
# st.title('Análise de texto')
extract_tab, predict_tab = st.tabs(['Extração e anotação', 'Predição e validação'])

# Section 1
extract_tab.header('Extração e anotação')
extract_tab.write('Essa página tem como intuito facilitar a extração e anotação de textos que \
            contenham qualquer tipo de violência contra mulheres.' )
extract_tab.markdown('---')

# Section 2
last_extraction_tweets = os.path.join(config.DATA_PATH_WRANGLE_TWEETS, 'last_extraction_tweets.parquet')
tweet, n_of_extracted_tweets_left = get_extracted_tweets(last_extraction_tweets)
extract_tab.text_area(f'Texto do tweet (Número de caracteres: {len(tweet["text"])}):', 
                      tweet['text'])
text_contain_vaw = extract_tab.radio(
    label='O texto acima possuí algum tipo de violência contra mulheres?',
    options =['Não', 'Somente uma parte', 'Sim', 'Descartar frase'],
    key='extract_tab',
    horizontal=True
)
if text_contain_vaw == 'Somente uma parte':
    tweet['text'] = extract_tab.text_input(
        label='Cole aqui a parte em que contém a agressão',
        placeholder='Ninguém vai acreditar em você')

if n_of_extracted_tweets_left > 0:
    next_text = extract_tab.button('Próximo texto')
    if next_text:  
        file_path = get_test_or_train_path(config.DATASET_TWEETS_TRAIN_FILE,
                                            config.DATASET_TWEETS_TEST_FILE,
                                            percentage_for_test=30)
        if text_contain_vaw == 'Não':
            tweet['label'] = 0
        else:
            tweet['label'] = 1
        if text_contain_vaw != 'Descartar frase':
            save_extracted_tweet(tweet, file_path)
        delete_extracted_tweet(last_extraction_tweets)
        st.experimental_rerun()

if tweet['text'] != 'Extraia mais textos':
    if extract_tab.button('Denunciar tweet!'):
        url = 'https://twitter.com/anyuser/status/{}'.format(tweet['id'])
        webbrowser.open_new_tab(url)

# Section 3
extract_tab.markdown('---')
extract_tab.markdown('*Todos textos que possuirem violência direcionada as mulheres serão utilizadas \
    para treino do algoritmo de machine learning*')
extract_tab.markdown('---')

# Body (predict_tab) =======================================================================================================
# Section 1
predict_tab.header('Predição e validação')
predict_tab.write('Essa página tem como intuito conferir se o algoritmo de machine learning \
            identificou corretamente se houve violência contra mulheres no texto analisado.' )
predict_tab.markdown('---')

# Section 2
predict_tab.subheader('Digite ou extraia uma frase para o modelo identificar se há ou não violência contra mulheres.')
text_to_predict = predict_tab.text_input(
        label='Digite uma frase para o modelo identificar se há ou não violência contra mulheres.',
        value=tweet['text'],
        label_visibility='hidden',
        )

if 'predict_button' not in st.session_state:
    st.session_state['predict_button'] = False

print(st.session_state)

predict_button = predict_tab.button('Identifique!')
if predict_button or st.session_state['predict_button']:
    set_button_to_true('predict_button')
    result = predict_text(text_to_predict)
    st.session_state['result'] = result
    if result == 1:
        predict_tab.markdown(":red[Foi identificado] uma ou mais agressões contra mulheres neste texto!")
        denounce_button = predict_tab.button('Denunciar tweet!', key='predict_denounce_button')
        if denounce_button:
            url = 'https://twitter.com/anyuser/status/{}'.format(tweet['id'])
            webbrowser.open_new_tab(url)
    else:
        predict_tab.markdown(":blue[Não foi identificado] agressões contra mulheres neste texto!")

    # Tofix: Para esse botão funcionar precisa de dois cliques
    delete_button = predict_tab.button('Próximo texto', key='predict_delete_button')
    if delete_button:
        was_deleted = delete_extracted_tweet(last_extraction_tweets)
        if was_deleted:
            set_button_to_false('predict_button')
            st.experimental_rerun()




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

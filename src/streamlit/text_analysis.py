import streamlit as st

import sys
sys.path.append('../data_scrap')
from data_scrap import extract_tweets, get_extracted_text, delete_extracted_text

# Streamlit page config
st.set_page_config(page_title='dvaw_annotation', page_icon=':violence')

# Sidebar
st.sidebar.header('Análise de texto')
text_contain_vaw = st.sidebar.select_slider(
    label='O texto em destaque ao lado possuí algum tipo de violência contra mulheres?',
    options =['Não', 'Sim'],
    value='Não'
)
st.sidebar.markdown('---')
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

# Body (extract_tab)
st.title('Análise de texto')
extract_tab, predict_tab = st.tabs(['Extração e anotação', 'Validação dos resultados preditos'])

extract_tab.header('Extração e anotação')
extract_tab.write('Essa página tem como intuito facilitar a extração e anotação de textos que \
            contenham qualquer tipo de violência contra mulheres.' )
extract_tab.code(get_extracted_text())
text_contain_vaw = extract_tab.select_slider(
    label='O texto acima possuí algum tipo de violência contra mulheres?',
    options =['Não', 'Sim', 'Somente uma parte'],
    value='Não',
    key='extract_tab'
)
if text_contain_vaw == 'Sim':
    extracted_agression_phrase = get_extracted_text()
elif text_contain_vaw == 'Somente uma parte':
    extracted_agression_phrase = extract_tab.text_input(
        label='Cole aqui a parte em que contém a agressão',
        placeholder='Ninguém vai acreditar em você')
else:
    extracted_agression_phrase = ''
next_text = extract_tab.button('Próximo texto')
if next_text:
    if extracted_agression_phrase:
        print(extracted_agression_phrase)
    
    delete_extracted_text()

extract_tab.markdown('*Todos textos que possuirem violência direcionada as mulheres serão utilizadas \
    para treino do algoritmo de machine learning*')
extract_tab.markdown('---')

# Body (predict_tab)
predict_tab.write('Essa página tem como intuito conferir se o algoritmo de machine learning \
            identificou corretamente se houve violência contra mulheres no texto analisado.' )
predict_tab.code('vai lavar louça sua vaca')
text_contain_vaw = predict_tab.select_slider(
    label='O texto acima possuí algum tipo de violência contra mulheres?',
    options =['Não', 'Sim'],
    value='Não',
    key='predict_tab'
)
predict_tab.write('Todos textos que possuirem violência direcionada as mulheres serão utilizadas \
    para criação de um dashboard para análise dos casos')
predict_tab.markdown('---')

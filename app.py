import streamlit as st
from joblib import load

# logo e título
st.image('img/bytebank_logo.png')
st.write('# Simulador de Avaliação de Crédito')

expander_trabalho = st.beta_expander('Trabalho')
expander_pessoal = st.beta_expander('Pessoal')
expander_familia = st.beta_expander('Família')

# carregando nossa lista de campos
lista_campos = load('objetos/lista_campos.joblib')

# dicionário para salvar as respostas do usuário
dict_respostas = {}

with expander_trabalho:
    col1_form, col2_form = st.beta_columns(2)

    dict_respostas['Categoria_de_renda'] = col1_form.selectbox('Qual a categotia de renda?', lista_campos['Categoria_de_renda'])

    dict_respostas['Rendimento_Anual'] = col1_form.slider('Qual o salário mensal?', min_value = 0, max_value = 35000, step = 500)

    dict_respostas['Tem_telefone_trabalho'] = 1 if col2_form.selectbox('Tem um telefone de trabalho?', ['Sim', 'Não']) == 'Sim' else 'Não'

#with expander_pessoal:

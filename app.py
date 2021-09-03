import streamlit as st
from joblib import load
import pandas as pd

# importando a classe Transformador para que o modelo funcione corretamente
from utils import Transformador

# Cor de fundo do listbox
st.markdown('<style> div[role = "listbox"] ul{background-color: #eee1f9e}; </style>', unsafe_allow_html = True)


# Função para avaliar o crédito utilizando o modelo de ML
def avaliar_mau(dict_respostas):
    # carregando o modelo
    modelo = load('objetos/modelo.joblib')
    # carregando as features
    features = load('objetos/features.joblib')

    # Tratando os dados
    if dict_respostas['Anos_desempregado'] > 0:
        dict_respostas['Anos_empregado'] = dict_respostas['Anos_desempregado'] * -1

    respostas = []

    # Salvando as respostas do usuário em uma lista de dicionários
    for coluna in features:
        respostas.append(dict_respostas[coluna])

    # Criando um dataframe com as features que o modelo utiliza e com as repostas do usuário
    df_novo_cliente = pd.DataFrame(data = [respostas], columns = features)
    mau = modelo.predict(df_novo_cliente)

    return mau

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
    dict_respostas['Ocupacao'] = col1_form.selectbox('Qual a ocupação?', lista_campos['Ocupacao'])
    dict_respostas['Tem_telefone_trabalho'] = 1 if col1_form.selectbox('Tem um telefone de trabalho?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Rendimento_Anual'] = col2_form.slider('Qual o salário mensal?', help = 'Podemos mover a barra usando as setas do teclado', min_value = 0, max_value = 35000, step = 500)
    dict_respostas['Anos_empregado'] = col2_form.slider('Quantos anos empregado?', help = 'Podemos mover a barra usando as setas do teclado', min_value = 0, max_value = 50, step = 1)
    dict_respostas['Anos_desempregado'] = col2_form.slider('Quantos anos desempregado?', help = 'Podemos mover a barra usando as setas do teclado', min_value = 0, max_value = 50, step = 1)

with expander_pessoal:
    col3_form, col4_form = st.beta_columns(2)

    dict_respostas['Grau_Escolaridade'] = col3_form.selectbox('Qual o grau de escolaridade?', lista_campos['Grau_Escolaridade'])
    dict_respostas['Estado_Civil'] = col3_form.selectbox('Qual o estado civil?', lista_campos['Estado_Civil'])
    dict_respostas['Tem_Carro'] = 1 if col3_form.selectbox('Tem carro?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Tem_telefone_fixo'] = 1 if col4_form.selectbox('Tem telefone fixo?', ['Sim', 'Não']) == 'Sim' else 0
    dict_respostas['Tem_email'] = 1 if col4_form.selectbox('Tem email?', ['Sim', 'Não']) == 'Sim' else 0
    dict_respostas['Idade'] = col4_form.slider('Qual a idade?', help = 'Podemos mover a barra usando as setas do teclado', min_value = 0, max_value = 100, step = 1)
    
with expander_familia:
    col5_form, col6_form = st.beta_columns(2)

    dict_respostas['Moradia'] = col5_form.selectbox('Qual o tipo de moradia?', lista_campos['Moradia'])
    dict_respostas['Tem_Casa_Propria'] = 1 if col5_form.selectbox('Tem casa própria?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Tamanho_Familia'] = col6_form.slider('Qual o tamanho da família?', min_value = 1, max_value = 20, step = 1)
    dict_respostas['Qtd_Filhos'] = col6_form.slider('Quantos filhos?', help = 'Podemos mover a barra usando as setas do teclado', min_value = 0, max_value = 20, step = 1)

# Criando um botão para enviar o formulário
if st.button('Avaliar crédito'):
    if avaliar_mau(dict_respostas):
        st.error('Crédito negado')
    else:
        st.success('Crédito aprovado')


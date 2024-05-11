import streamlit as st
st.set_page_config(page_title='ConfereAqui', page_icon='🔍', layout='wide')
from pathlib import Path
from google.generativeai import genai
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import os
load_dotenv()
from PIL import Image
import io
import os

# Configurando o título do aplicativo
st.title("Verificador de Notícias")

# Configuração do SDK com as configurações de segurança
GOOGLE_API_KEY = "AIzaSyA5oYJp9yMKID2lBqo9gdkIbpX23IIsGhw"
genai = genai(api_key=GOOGLE_API_KEY)

# Lista para armazenar o histórico de respostas
if "historico_respostas" not in st.session_state.keys():
    st.session_state.historico_respostas = []

# Contador de respostas
if "resposta_counter" not in st.session_state.keys():
    st.session_state.resposta_counter = 0

# Widgets para upload de imagens e inserção de texto
upload_button = st.file_uploader("Faça upload de uma imagem/vídeo")
text_input = st.text_area("Insira o texto da sua notícia aqui")

# Mensagem de "Gerando resposta..."
gerando_resposta_msg = st.empty()

# Função para lidar com o clique no botão "Verificar Notícia"
if st.button("Verificar Notícia"):

    content = None
    if upload_button:
        img = Image.open(upload_button)
        content = img
    elif text_input:
        content = text_input

    if content:
        # Exibir a mensagem "Gerando resposta..."
        gerando_resposta_msg.text("Gerando resposta...")

        st.session_state.resposta_counter += 1
        # Gerar o conteúdo com o modelo de visão do Gemini
        model_vision = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model_vision.generate_content(["Você é um modelo de linguagem projetado para detectar desinformação. Analise o seguinte texto de notícias, forneça uma pontuação de desinformação de 0 a 1, onde 1 é altamente provável de ser desinformação e adicione evidências de apoio.", content], stream=True)

        # Resolver a resposta
        response.resolve()

        # Imprimir o texto gerado pelo modelo com a classificação da resposta
        resposta_texto = f"**Resposta {st.session_state.resposta_counter}:** {response.text}"

        # Adicionar a resposta ao histórico
        st.session_state.historico_respostas.append(resposta_texto)

        # Esconder a mensagem "Gerando resposta..."
        gerando_resposta_msg.empty()

# Exibir histórico de respostas
if st.session_state.historico_respostas:
    st.subheader("Histórico de Respostas")
    for resposta in st.session_state.historico_respostas:
        st.write(resposta)

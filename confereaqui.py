import streamlit as st
st.set_page_config(page_title='ConfereAqui', page_icon='🔍', layout='wide')
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import os
load_dotenv()
from PIL import Image
import io
import os

system_instruction = "Você é um modelo de linguagem projetado para detectar desinformação. Analise o seguinte texto de notícias, forneça uma pontuação de desinformação de 0 a 1, onde 1 é altamente provável de ser desinformação e adicione evidências de apoio."

# Configuração do SDK com as configurações de segurança
GOOGLE_API_KEY = "AIzaSyA5oYJp9yMKID2lBqo9gdkIbpX23IIsGhw"
genai.configure(api_key=api_key=GOOGLE_API_KEY)

safety_settings = {
        "HARASSMENT" : "BLOCK_NONE",
    
        "HATE" : "BLOCK_NONE",
  
        "SEXUAL" : "BLOCK_NONE",
    
        "DANGEROUS" : "BLOCK_NONE",
    }

# Configurando a api para o modelo
genai.configure(api_key=GOOGLE_API_KEY("gemini_api_key"))
# Inicializando o modelo (gemini-1.5-pro-latest)
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro-latest",
  system_instruction=system_instruction
                              )

initial_model_message = "Olá eu sou Robson um assistente virtual que te ajuda a encontrar a vaga de emprego ideal para você com processo seletivo aberto. Como você se chama?"

# Fazendo o display do título da página
st.title('EmpregoConnect🕵️')


for i, message in enumerate(st.session_state.chat.history):
  if i == 1:
     continue
  if message.role == "user":
    with st.chat_message("user"):
      st.markdown(message.parts[0].text)
  else:
    with st.chat_message("assistant"):
      st.markdown(message.parts[0].text)

user_query = st.chat_input('Você pode falar ou digitar sua resposta aqui:') 

chat = model.start_chat()

if user_query is not None and user_query != '':
    # st.session_state.chat_history.append(("user", user_query))
    
    with st.chat_message("user"):
      st.markdown(user_query)
    
    with st.chat_message("assistant"):

      ai_query = st.session_state.chat.send_message( user_query ).text

      st.markdown(ai_query)

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

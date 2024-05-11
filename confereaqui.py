import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import os

system_instruction = "Você é um modelo de linguagem projetado para detectar desinformação. Analise o seguinte texto de notícias, forneça uma pontuação de desinformação de 0 a 1, onde 1 é altamente provável de ser desinformação e adicione evidências de apoio."

# Configuração do SDK com as configurações de segurança
GOOGLE_API_KEY = "AIzaSyA5oYJp9yMKID2lBqo9gdkIbpX23IIsGhw"
genai.configure(api_key=GOOGLE_API_KEY)
safety_settings = {
        "HARASSMENT" : "BLOCK_NONE",
        "HATE" : "BLOCK_NONE",
        "SEXUAL" : "BLOCK_NONE",
        "DANGEROUS" : "BLOCK_NONE",
    }

# Configurando a página
st.set_page_config(page_title='ConfereAqui', page_icon='🔍', layout='wide')

# Fazendo o display do título da página
st.title('Confere Aqui 🔍')

# Texto de introdução e instrução de utilização
st.markdown("""
    Bem-vindo ao Confere Aqui!\n Sou projetado para verificar a veracidade de notícias.\n 
    \n Você pode fazer upload de uma imagem ou inserir o texto de uma notícia para verificar se há desinformação.
    \n Após fazer o upload ou inserir o texto, clique no botão "Verificar Notícia" para obter uma análise.
""")

# Inicializando o modelo
system_instruction = "Você é um modelo de linguagem projetado para detectar desinformação. Analise o seguinte texto de notícias, forneça uma pontuação de desinformação de 0 a 1, onde 1 é altamente provável de ser desinformação e adicione evidências de apoio."
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction=system_instruction
)

# Inicialização do estado
if "historico_respostas" not in st.session_state:
    st.session_state.historico_respostas = []

if "resposta_counter" not in st.session_state:
    st.session_state.resposta_counter = 0

# Widget para upload de imagens
upload_button = st.file_uploader("Faça upload de uma imagem" )
text_input = st.text_area("Ou insira o texto da sua notícia aqui")

# Mensagem de "Gerando resposta..."
gerando_resposta_msg = st.empty()

# Função para lidar com o clique no botão "Verificar Notícia"
if st.button("Verificar Notícia"):
    content = None
    if upload_button is not None:
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

        # Limpar o campo de texto
        text_input = ""  # Define o campo de texto como vazio

        # Esconder a mensagem "Gerando resposta..."
        gerando_resposta_msg.empty()
            
# Exibir histórico de respostas em formato de chat
if st.session_state.historico_respostas:
    for i, resposta in enumerate(st.session_state.historico_respostas):
        if i % 2 == 0:
            # Exibe a mensagem enviada pelo usuário
            with st.beta_container():
                st.markdown(f"**Usuário:** {user_query}")
        else:
            # Exibe a resposta do assistente
            with st.beta_container():
                st.markdown(f"**Assistente:** {resposta}")



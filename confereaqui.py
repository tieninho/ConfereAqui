import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import os

# Instrução do sistema
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
    🔍 **Bem-vindo ao Confere Aqui!**

    Este é o seu detector de desinformação, pronto para ajudá-lo a navegar pelo mar de notícias com confiança. O objetivo é garantir que você possa identificar conteúdos duvidosos e tomar decisões informadas.

    ℹ️ **Como funciona?**

    Você pode nos fornecer um texto de notícia ou até mesmo fazer o upload de uma imagem relacionada. Nosso sistema analisará o conteúdo, atribuindo uma pontuação de desinformação de 0 a 1. Quanto mais próximo de 1, maior a probabilidade de ser desinformação.

    ⚠️ **Importante:**

    Lembre-se de que somos um modelo inicial e nossa análise não substitui a verificação em fontes de notícias confiáveis. Sempre verifique as informações em sites de notícias respeitáveis antes de tirar conclusões.

    ✅ Com o Confere Aqui, você pode navegar pelas notícias com confiança, sempre pronto para separar os fatos da ficção!

""")

# Título "Teste Agora:"
st.header("Teste agora:")

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
text_input = st.text_area("Ou insira o texto da sua notícia aqui", key="texto")

# Mensagem de "Gerando resposta..."
gerando_resposta_msg = st.empty()

# Função para lidar com o clique no botão "Verificar Notícia"
if st.button("Verificar Notícia"):
    content = None
    if upload_button is not None and text_input:
        st.error("Por favor, selecione apenas um método de entrada: imagem ou texto.")
    elif upload_button is not None:
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
    st.subheader("Resultado 🔍")
    # Iterar sobre o histórico de respostas de trás para frente
    for resposta in reversed(st.session_state.historico_respostas):
        st.write(resposta)
        st.markdown("---")  # Linha divisória entre as respostas

# Botão para limpar o upload da imagem e o texto inserido
if st.button("Limpar"):
    st.session_state.texto = ""

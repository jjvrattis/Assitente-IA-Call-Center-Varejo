import streamlit as st
from langchain_community.document_loaders import CSVLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
import os

# 🎯 Carregar API Key de forma segura
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# 🌿 Estilo personalizado
st.set_page_config(page_title="Assistente Caedu ", layout="centered")
st.markdown("""
<style>
    body { background-color: #e7f5ec; }
    .stTextArea > div > textarea {
        background-color: #f0fff0;
        border: 1px solid #90ee90;
        border-radius: 6px;
    }
    .stButton > button {
        background-color: #2e8b57;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
    }
    .green-container {
        background-color: #d1f2d1;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #228B22;
        font-size: 1.1em;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# 🧠 Sidebar com histórico
with st.sidebar:
    st.title("📚 Histórico de Dúvidas")
    
    # Botão para limpar
    if st.button("🧹 Limpar histórico"):
        st.session_state["historico"] = []

    # Mostrar histórico, se existir
    for i, item in enumerate(st.session_state.get("historico", []), 1):
        st.markdown(f"**{i}.** {item}")

st.title("Tá com duvida? Pergunte ao Cadu 😉")

# 📤 Upload de CSV customizado
#uploaded_file = st.file_uploader("📄 Envie qualquer Arquivo CSV", type="csv")
#if uploaded_file:
    #file_path = "uploaded_base.csv"
    #with open(file_path, "wb") as f:
        #if.write(uploaded_file.getbuffer())
#else:
file_path = os.path.join(os.path.dirname(__file__), "Base_caedu.csv")

# 📦 Carregar documentos
try:
    loader = CSVLoader(file_path=file_path, encoding="latin1")
    documents = loader.load()
    #st.success("✅ Base de dados carregada.")
except Exception as e:
    st.error(f"❌ Erro ao carregar CSV: {e}")
    st.stop()

# 🔎 Função de busca simplificada em memória
def retrive_info(query):
    return [
        doc.page_content
        for doc in documents
        if query.lower() in doc.page_content.lower()
    ]

# ✏️ Template de Prompt
template = """
VVocê é uma assistente virtual para operadores de call center da Caedu. Seu papel é responder dúvidas sobre cobrança, usando trechos extraídos de uma base de dados real.

⚠️ Regras:
1. Responda apenas sobre Caedu, mesmo que a dúvida seja externa.
2. Use obrigatoriamente os trechos abaixo como referência.
3. Ajude com foco em jovens de 16 a 23 anos, com linguagem clara e acessível.
4. Seu nome é Cadu.

🗨️ Mensagem recebida:
{message}

📚 Trechos extraídos da base:
{best_practice}

✍️ Escreva uma resposta que o operador possa repetir ao cliente, mantendo clareza e cordialidade:
"""
prompt = PromptTemplate(input_variables=["message", "best_practice"], template=template)
llm = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
chain = prompt | llm

# 🧪 Interface
# 🧪 Interface
user_input = st.text_area("Digite a dúvida recebida pelo operador:")
if st.button("💡 Gerar resposta"):
    with st.spinner("Pensando na melhor resposta..."):
        best_practice = retrive_info(user_input)
        resposta = chain.invoke({
            "message": user_input,
            "best_practice": "\n".join(best_practice)
        })

    # ✅ Salvar dúvida no histórico da sessão
    if "historico" not in st.session_state:
        st.session_state["historico"] = []
    st.session_state["historico"].append(user_input)

    # 🧠 Mostrar resposta
    st.markdown("### 🧠 Resposta sugerida:")
    st.markdown(f"<div class='white-container'>{resposta.content}</div>", unsafe_allow_html=True)

    with st.expander("📚 Trechos usados como base"):
        for i, trecho in enumerate(best_practice, 1):
            st.markdown(f"**{i}.** {trecho}")

    with st.expander("📚 Trechos usados como base"):
        for i, trecho in enumerate(best_practice, 1):
            st.markdown(f"**{i}.** {trecho}")

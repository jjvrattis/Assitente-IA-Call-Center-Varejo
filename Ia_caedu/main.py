import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
import os

# 🎯 Carregar API Key de forma segura
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# 🌿 Estilo personalizado
st.set_page_config(page_title="Assistente Caedu", layout="centered")
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

st.title("🌿 Assistente de Cobrança - Caedu")

# 📤 Upload de CSV customizado
uploaded_file = st.file_uploader("📄 Envie o FAQ da Caedu em CSV", type="csv")
if uploaded_file:
    file_path = "uploaded_base.csv"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
else:
    file_path = os.path.join(os.path.dirname(__file__), "Base_caedu.csv")  # fallback padrão

# 📦 Carregar documentos
try:
    loader = CSVLoader(file_path=file_path, encoding="latin1")
    documents = loader.load()
    st.success("✅ Base de dados carregada.")
except Exception as e:
    st.error(f"❌ Erro ao carregar CSV: {e}")
    st.stop()

# 🔍 Embeddings + Vetor
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
db = FAISS.from_documents(documents, embeddings)

# 🔎 Função de busca
def retrive_info(query):
    results = db.similarity_search(query, k=3)
    return [doc.page_content for doc in results]

# ✏️ Template de Prompt
template = """
Você é uma assistente virtual para operadores de call center focada na carteira de cobrança da Caedu.
Sua função é auxiliar com dúvidas de Operadores e revisar scripts.

⚠️ Regras:
1. Responda apenas sobre Caedu, invente desculpas para temas externos.
2. Seja direto(a) e gentil.
3. Ajude com foco em jovens de 16 a 23 anos.
4. Seu nome é Cadu.

🗨️ Mensagem recebida:
{message}

📚 Material de apoio:
{best_practice}

✍️ Escreva a melhor resposta possível para apoiar o operador:
"""

prompt = PromptTemplate(input_variables=["message", "best_practice"], template=template)
llm = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
chain = prompt | llm

# 🧪 Interface
user_input = st.text_area("Digite a dúvida recebida pelo operador:")
if st.button("💡 Gerar resposta"):
    with st.spinner("Pensando na melhor resposta..."):
        best_practice = retrive_info(user_input)
        resposta = chain.invoke({
            "message": user_input,
            "best_practice": "\n".join(best_practice)
        })

    # 🧠 Mostrar resposta em container verde
    st.markdown("### 🧠 Resposta sugerida:")
    st.markdown(f"<div class='green-container'>{resposta.content}</div>", unsafe_allow_html=True)

    # 📚 Mostrar trechos usados
    with st.expander("📚 Trechos usados como base"):
        for i, trecho in enumerate(best_practice, 1):
            st.markdown(f"**{i}.** {trecho}")

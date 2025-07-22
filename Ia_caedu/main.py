import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate

# 🎯 Carregar variáveis de ambiente
load_dotenv()

# 🏷️ Interface
st.set_page_config(page_title="Assistente Caedu", layout="centered")
st.title("🌿 Assistente de Cobrança - Caedu")

# 📤 Upload de CSV customizado
file_path = "Base_caedu.csv"  # fallback padrão

# 📦 Carregar documentos

loader = CSVLoader(file_path=file_path, encoding="latin1")
documents = loader.load()
 

# 🧠 Embeddings + Vetor
embeddings = OpenAIEmbeddings()
db = Chroma.from_documents(documents, embeddings)

# 🔍 Função de busca
def retrive_info(query):
    results = db.similarity_search(query, k=3)
    return [doc.page_content for doc in results]

# 📜 Template de Prompt
template = """
Você é uma assistente virtual para operadores de call center focada na carteira de cobrança da Caedu.
Sua função é auxiliar com dúvidas de Operadores e revisar scripts.

⚠️ Regras:
1. Responda apenas sobre Caedu, invente desculpas para temas externos.
2. Seja direto(a) e gentil.
3. Ajude com foco em jovens de 16 a 23 anos.
4. Seu nome e Cadu
🗨️ Mensagem recebida:
{message}

📚 Material de apoio:
{best_practice}

✍️ Escreva a melhor resposta possível para apoiar o operador:
"""
prompt = PromptTemplate(input_variables=["message", "best_practice"], template=template)
llm = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo")
chain = prompt | llm

# 🧪 Geração de resposta
user_input = st.text_area("Digite a dúvida recebida pelo operador:")

if st.button("💡 Gerar resposta"):
    with st.spinner("Pensando na melhor resposta..."):
        best_practice = retrive_info(user_input)
        resposta = chain.invoke({
            "message": user_input,
            "best_practice": "\n".join(best_practice)
        })

    # 🧠 Mostra a resposta dentro de um container verde
    st.markdown("### 🧠 Resposta sugerida:")
    st.markdown(f"<div class='green-container'>{resposta.content}</div>", unsafe_allow_html=True)

    # 📚 Trechos de apoio
    with st.expander("📚 Trechos usados como base"):
        for i, trecho in enumerate(best_practice, 1):
            st.markdown(f"**{i}.** {trecho}")

    #with st.expander("📚 Trechos usados como base"):
        #for i, trecho in enumerate(best_practice, 1):
           # st.markdown(f"**{i}.** {trecho}")
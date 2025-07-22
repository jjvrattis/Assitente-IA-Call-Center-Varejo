# Assitente-IA-Call-Center-Varejo

Este projeto utiliza inteligência artificial com LangChain, Streamlit e OpenAI para auxiliar operadores da carteira de cobrança da Caedu. A IA responde dúvidas com base em uma planilha de perguntas e respostas atualizada automaticamente.

---

## 🚀 Funcionalidades

- Respostas automáticas treinadas com material da Caedu
- Interface interativa com Streamlit
- Upload dinâmico de planilha CSV com FAQs
- Busca por vetores semânticos com embeddings
- Interface estilizada com tema verde
- Atualização contínua dos dados
- Container especial para exibir respostas da IA

---

## 🧱 Tecnologias usadas

| Componente     | Descrição                                           |
|----------------|-----------------------------------------------------|
| Streamlit      | Interface web interativa para operadores            |
| LangChain      | Framework de orquestração dos LLMs                  |
| OpenAI         | API GPT-3.5 para geração de respostas               |
| FAISS/Chroma   | Vetorização e busca de similaridade semântica       |
| dotenv         | Gerenciamento seguro das credenciais                |
| CSVLoader      | Leitura e ingestão de dados da planilha Caedu       |

---

## 📦 Como instalar

1. Clone o repositório:
```bash
git clone https://github.com/jjvsrattis/Assitente-IA-Call-Center-Varejo.git
cd Assitente-IA-Call-Center-Varejo
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

> Se estiver usando Python 3.12, atenção para compatibilidade com `faiss`.

3. Configure sua chave da OpenAI:
Crie um arquivo `.env` com:
```env
OPENAI_API_KEY=sk-xxxxxx
```

---

## ▶️ Como rodar

```bash
streamlit run main.py
```

> O app vai abrir automaticamente no navegador!

---

## 📁 Estrutura do projeto

```
├── main.py               # Código principal da IA e interface
├── Base_caedu.csv        # Planilha com dados de perguntas e respostas
├── .env                  # Chave secreta da OpenAI
├── README.md             # Documentação do projeto
```

---

## 💡 Personalizações possíveis

- Adicionar log de produtividade por operador
- Exportar histórico de dúvidas e respostas
- Integração com Google Sheets ao invés de CSV local
- Versão mobile e modo supervisão

---

## 🧠 Créditos

Projeto desenvolvido por João Rattis com o apoio da assistente virtual da Microsoft Para Otimização do Doc

---

## 📜 Licença

Este projeto é privado e exclusivo da equipe Caedu. Uso restrito a operadores autorizados.
```

---



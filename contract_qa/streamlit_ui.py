from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_openai import ChatOpenAI
import streamlit as st

st.set_page_config(page_title="Insurance Contract QA", page_icon="📄")
st.title("📄 Insurance Contract QA Agent")

# --- Embeddings Setup: using Ollama with nomic-embed-text ---
embedding = OllamaEmbeddings(model="nomic-embed-text") 

# --- Load the persisted vector store ---
vector_store = Chroma(persist_directory="./home_chroma_ollama", embedding_function=embedding)


# --- Setup QA Chain ---
def get_qa_chain():
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )


# --- UI and Query Handling ---
query = st.text_input("Ask a question about the insurance contract:")

if query:
    with st.spinner("Searching..."):
        chain = get_qa_chain()
        result = chain(query)

        st.subheader("Answer:")
        st.write(result["result"])

        st.subheader("Sources:")
        for i, doc in enumerate(result["source_documents"]):
            st.markdown(f"**Chunk {i + 1}**")
            st.code(doc.page_content.strip(), language="markdown")

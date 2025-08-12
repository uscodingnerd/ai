from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings

# Step 1: Load the document
loader = TextLoader("insurance_contract.txt", encoding="utf-8")
docs = loader.load()

# Step 2: Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
documents = splitter.split_documents(docs)

# Step 3: Use Ollama with Nomic embedding model
embedding = OllamaEmbeddings(model="nomic-embed-text")

# Step 4: Store documents in Chroma vector store
vector_store = Chroma.from_documents(documents, embedding, persist_directory="./home_chroma_ollama")

# Step 5: Persist the vector store to disk
vector_store.persist()

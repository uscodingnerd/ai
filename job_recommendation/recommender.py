from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from database import SessionLocal
from models import JobPosting


def build_vector_index():
    session = SessionLocal()
    jobs = session.query(JobPosting).all()

    texts = [job.description for job in jobs]
    metadatas = [{"id": job.id, "title": job.title} for job in jobs]

    embeddings = OpenAIEmbeddings()
    faiss_index = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    faiss_index.save_local("faiss_index")


def recommend_jobs(query: str, k: int = 5):
    embeddings = OpenAIEmbeddings()
    faiss_index = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    return faiss_index.similarity_search(query, k=k)


def recommend_jobs_with_scores(query: str, k: int = 5):
    embeddings = OpenAIEmbeddings()
    faiss_index = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    return faiss_index.similarity_search_with_score(query, k=k)

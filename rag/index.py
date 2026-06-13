from pathlib import Path
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path)

if not os.getenv("OPENAI_API_KEY") and os.getenv("OPEN_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_API_KEY")

path_to_rag = Path(__file__).parent / "nodejs.pdf"
print(f"Path to RAG PDF: {path_to_rag}")

# load this file to python program

loader = PyPDFLoader(file_path=str(path_to_rag))
docs = loader.load()
print(f"Number of documents loaded: {len(docs)}")
print(docs[0])

# split the document into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents = docs)

# vectorize the chunks using OpenAI embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    collection_name="nodejs_rag",
    url = "http://localhost:6333"
)

print("Vector store created and documents added successfully.")
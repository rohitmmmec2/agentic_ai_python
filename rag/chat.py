from langchain_openai import OpenAIEmbeddings
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI


dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path)

if not os.getenv("OPENAI_API_KEY") and os.getenv("OPEN_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_API_KEY")

openai_client = OpenAI()

# vectorize the chunks using OpenAI embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    collection_name="nodejs_rag",
    url="http://localhost:6333"
)

user_query = input("Enter your question about Node.js: ")
# return the most relevant documents based on the user query
searched_docs = vector_store.similarity_search(user_query)

context = "\n\n".join([f"Page content: {doc.page_content}\n Page Number: {doc.metadata['page_label']}\nPage link: {doc.metadata['source']}" for doc in searched_docs])

SYSTEM_PROMPT = """You are a helpful assistant that provides information about Node.js
along with page content and page links and inform user to get more information by opening the page based on the following documents: {context}"""

response =openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
        {"role": "user", "content": user_query}
    ])

print("Answer:")
print(response.choices[0].message.content)
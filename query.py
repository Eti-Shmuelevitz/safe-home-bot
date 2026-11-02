import truststore
truststore.inject_into_ssl()

from dotenv import load_dotenv
import chromadb
from llama_index.core import VectorStoreIndex, Settings, PromptTemplate
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.vector_stores.chroma import ChromaVectorStore

load_dotenv()


Settings.embed_model = GoogleGenAIEmbedding(model_name="gemini-embedding-001")
Settings.llm = GoogleGenAI(model="gemini-3.1-flash-lite")


client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("safe_home")
vector_store = ChromaVectorStore(chroma_collection=collection)
index = VectorStoreIndex.from_vector_store(vector_store)


qa_prompt = PromptTemplate(
    "אתה נציג שירות של חברת 'בטוח בבית'.\n"
    "ענה בעברית, אך ורק לפי המידע שלהלן.\n"
    "אם התשובה לא מופיעה במידע, ענה: 'אין לי מידע על כך. אפשר לפנות לשירות הלקוחות במספר 5050*.'\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "שאלה: {query_str}\n"
    "תשובה: "
)


query_engine = index.as_query_engine(similarity_top_k=4, text_qa_template=qa_prompt)

def ask(question):
    response = query_engine.query(question)
    return str(response)


if __name__ == "__main__":
    print(ask("כמה עולה המנוי החודשי?"))
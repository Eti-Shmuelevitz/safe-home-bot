import truststore
truststore.inject_into_ssl()
from dotenv import load_dotenv
import chromadb
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

load_dotenv()

Settings.embed_model = GoogleGenAIEmbedding(model_name="gemini-embedding-001")


documents = SimpleDirectoryReader("data").load_data()
print("documents:", len(documents))


splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("safe_home")
vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


VectorStoreIndex.from_documents(documents, storage_context=storage_context, transformations=[splitter])
print("done")
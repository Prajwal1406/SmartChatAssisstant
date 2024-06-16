from pinecone.grpc import PineconeGRPC as pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import SentenceTransformerEmbeddings
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
load_dotenv()
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_API_ENV = os.getenv('PINECONE_API_ENV')

index_name = "sample3"
# initiate the model object
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

pc = pinecone(api_key=PINECONE_API_KEY)

def ensure_index_exists():
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud='aws', 
                region='us-east-1'
            ) 
        )

# initilize the pinecone
ensure_index_exists()
index = pc.Index(index_name)
vectorstore = PineconeVectorStore(index_name=index_name, embedding=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2"))
# load the corpus and encode each chunks
def encodeaddData(corpusData, url, pdf, pdf2):
    #id = index.describe_index_stats()["total_vector_count"]
    if url:
        class Document:
            def __init__(self, page_content, metadata):
                self.page_content = page_content
                self.metadata = metadata

# Create a list of Document objects
        documents = [Document(text, {}) for text in corpusData]

        # Now you can create the vector store with the properly structured documents
        vectorstore = PineconeVectorStore.from_documents(documents, embeddings, index_name=index_name)
    if pdf:
        class Document:
            def __init__(self, page_content, metadata):
                self.page_content = page_content
                self.metadata = metadata

# Create a list of Document objects
        documents = [Document(text, {}) for text in corpusData]

        # Now you can create the vector store with the properly structured documents
        vectorstore = PineconeVectorStore.from_documents(documents, embeddings, index_name=index_name)
    if pdf2:
        class Document:
            def __init__(self, page_content, metadata):
                self.page_content = page_content
                self.metadata = metadata

# Create a list of Document objects
        documents = [Document(text, {}) for text in corpusData]

        # Now you can create the vector store with the properly structured documents
        vectorstore = PineconeVectorStore.from_documents(documents, embeddings, index_name=index_name)
        

def delete():
    pc.delete_index(index_name)
# find the best match from index    
# def find_k_best_match(query,k):
#     result = vectorstore.similarity_search(query)
#     return [result['matches'][i]['metadata']['title'] for i in range(k)],[result['matches'][i]['metadata']['context'] for i in range(k)]
def find_k_best_match1(query):        
    vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
    docs = vectorstore.similarity_search(query,k=2)
    # print(docs)
    return docs
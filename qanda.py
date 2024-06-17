import os
from dotenv import load_dotenv
from pinecone.grpc import PineconeGRPC as Pinecone
from vector_search import ensure_index_exists
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import SentenceTransformerEmbeddings
load_dotenv()
ensure_index_exists()
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
index_name = "sample3"
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
# index = pc.Index(index_name)
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_API_ENV = os.getenv('PINECONE_API_ENV')
os.environ['PINECONE_API_ENV'] = PINECONE_API_ENV
os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

# define a prompt
vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)

def prompt(context, query):
    header = "Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text and requires some latest information to be updated, print 'Sorry Not Sufficient context to answer query' \n"
    return header + context + "\n\n" + query + "\n"   

# feed the prompt to the model to return the answer using openai's compleation api
def get_answer(promt):
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.chains import RetrievalQA
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro",convert_system_message_to_human=True)

    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())

    response = qa.invoke(promt)
    return response['result']

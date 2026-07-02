import os
from turtle import st
from langchain_core import documents
from langchain_mistralai import ChatMistralAI, embeddings
# Use the Chroma vectorstore from langchain's vectorstores package
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "meeting_transcripts"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"}
    )

def build_vector_store(transcript:str) -> Chroma:

    print(f"Building vector store for transcript...")


    splitter = RecursiveCharacterTextSplitter(
        chunk_size= 1000,
        chunk_overlap=200
    )
    chunks = splitter.split_text(transcript)
    

    docs = [
        Document(page_content=chunk, metadata={'chunk_index': i}) for i, chunk in enumerate(chunks)
    ]

    embedding_model = get_embeddings()


    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME
    )

    return vector_store

def load_vector_store() ->Chroma:
    embeddings = get_embeddings()
    vector_store = Chroma(
        collection_name= COLLECTION_NAME,
        embedding_function= embeddings,
        persist_directory= CHROMA_DIR
    )

    return vector_store

def get_retriever(vector_store : Chroma, k:int =8):
    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": k,
            "fetch_k": 20,
            "lambda_mult": 0.7
        }   
    )

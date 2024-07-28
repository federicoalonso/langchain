import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_openai.embeddings import OpenAIEmbeddings

load_dotenv()


if __name__ == '__main__':
    loader = TextLoader("/home/falonso/Documentos/GitHub/langchain/03-rag/medium-blog-1.txt")
    document = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    chunks = text_splitter.split_documents(document)

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    PineconeVectorStore.from_documents(chunks, embeddings, index_name=os.getenv("INDEX_NAME"))
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_ollama.llms import OllamaLLM
from langchain_pinecone import PineconeVectorStore

from langchain import hub

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

load_dotenv()

if __name__ == '__main__':
    embeddings = OpenAIEmbeddings()
    llm = ChatOpenAI()
    model = OllamaLLM(model="llama3.1")

    query = "How can i convert text to images?"
    chain = PromptTemplate.from_template(template=query) | model
    result = chain.invoke(input={})
    print(result)

    print("******************************************************")

    vectorstore = PineconeVectorStore(
        index_name=os.getenv("INDEX_NAME"), embedding=embeddings
    )

    # Prompt con el que va a contestar
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    # Combina los documentos con el prompt
    combine_docs_chain = create_stuff_documents_chain(model, retrieval_qa_chat_prompt)
    # Obtiene los documentos
    retrieval_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(), combine_docs_chain=combine_docs_chain
    )

    result = retrieval_chain.invoke(input={"input": query})
    print(result)
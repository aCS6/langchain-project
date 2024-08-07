# First Run the seeder.py file manually for first time
from langchain_openai import AzureChatOpenAI
from langchain import hub
from langchain_community.vectorstores import Chroma
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# from langchain.chains.retrieval_qa.base import RetrievalQA

# Has depreciation warning
from langchain.chains.llm import LLMChain

from seeder import embeddings, DB_PERSIST_DIRECTORY
from redundant_filter_receiver import RedundantFilterRetriever

from dotenv import load_dotenv
import os

import langchain

langchain.debug = True

# Load environment variables from .env file
load_dotenv()

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
api_key = os.environ["API_KEY"]

# Chat
chat = AzureChatOpenAI(
    api_key=api_key,
    azure_deployment=deployment,
    api_version="2024-02-01",
)

db = Chroma(persist_directory=DB_PERSIST_DIRECTORY, embedding_function=embeddings)
retriever = RedundantFilterRetriever(embeddings=embeddings, chroma=db)

retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

combine_docs_chain = create_stuff_documents_chain(chat, retrieval_qa_chat_prompt)
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

result = retrieval_chain.invoke("Tell me something about Bangladesh?")

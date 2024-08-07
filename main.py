# Import necessary classes and functions from langchain and other modules
from langchain_openai import AzureChatOpenAI
from langchain import hub
from langchain_community.vectorstores import Chroma
from langchain.chains.retrieval_qa.base import RetrievalQA
from seeder import embeddings, DB_PERSIST_DIRECTORY
from redundant_filter_receiver import RedundantFilterRetriever
from dotenv import load_dotenv
import os

# Uncomment the following lines for debugging purposes if needed
# import langchain
# langchain.debug = True

# Load environment variables from .env file
load_dotenv()

# Retrieve necessary environment variables
endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
api_key = os.environ["API_KEY"]

# Initialize the AzureChatOpenAI chat model
chat = AzureChatOpenAI(
    api_key=api_key,
    azure_deployment=deployment,
    api_version="2024-02-01",
)

# Initialize the Chroma vector store with persistence directory and embedding function
db = Chroma(persist_directory=DB_PERSIST_DIRECTORY, embedding_function=embeddings)

# Initialize the custom retriever with redundant filter using the embeddings and Chroma database
retriever = RedundantFilterRetriever(embeddings=embeddings, chroma=db)

# Create a RetrievalQA chain with the chat model and retriever
chain = RetrievalQA.from_chain_type(llm=chat, retriever=retriever, chain_type="stuff")

# Query the chain with a question about the old name of Sri Lanka and get the result
result = chain.invoke("What is the old name of Srilanka?")

# Print the result
print(result["result"])

from langchain.prompts import (
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langchain_community.document_loaders import TextLoader

# Has depreciation warning
from langchain.chains.llm import LLMChain

from dotenv import load_dotenv
import os

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

loader = TextLoader("facts.txt")
docs = loader.load()

print(docs)
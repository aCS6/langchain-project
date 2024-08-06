from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI, AzureOpenAI
from langchain_core.memory import ConversationBufferWindowMemory

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

memory = ConversationBufferWindowMemory()

# We can also specify 'k' parameter here. `k` means last how many chat we want to save
# memory = ConversationBufferWindowMemory(k=2)

conversation = ConversationChain(llm=chat, memory=memory, verbose=True)

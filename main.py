from langchain.prompts import (
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationSummaryMemory

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

memory = ConversationSummaryMemory(
    memory_key="messages",
    return_messages=True,
    llm=chat
)
prompt = ChatPromptTemplate(
    input_variables=["content", "messages"],
    messages=[
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{content}")
    ]
)

chain = LLMChain(
    llm=chat,
    prompt=prompt,
    memory=memory,
    verbose=True
)

while True:
    content = input(">> ")

    result = chain({"content": content})

    print(result["text"])
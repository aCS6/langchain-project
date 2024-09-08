from langchain_openai import AzureChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import SystemMessage
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
from tools.sql import run_query_tool, list_tables, describe_tables_tool
from tools.report import write_report_tool
from handlers.chat_model_start_handler import ChatModelStartHandler

load_dotenv()
endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
api_key = os.environ["API_KEY"]

chat_model_start_hadler = ChatModelStartHandler()

chat = AzureChatOpenAI(
    api_key=api_key,
    azure_deployment=deployment,
    api_version="2024-02-01",
    callbacks=[chat_model_start_hadler],
)

tables = list_tables()
prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(
            content=(
                "You are an AI that has access to a SQLite database.\n"
                f"The database has tables of: {tables}\n"
                "Do not make any assumptions about what tables exist "
                "or what columns exist. Instead, use the 'describe_tables' function"
            )
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
tools = [run_query_tool, describe_tables_tool, write_report_tool]

agent = create_openai_functions_agent(llm=chat, prompt=prompt, tools=tools)

agent_executor = AgentExecutor(
    agent=agent,
    # verbose=True,
    tools=tools,
    memory=memory,
)

agent_executor.invoke(
    {"input": "Which products price are below 11? Write the result to an html report."}
)

# agent_executor.invoke({"input": "Repeat the exact same process for users."})

import os
import argparse
from operator import itemgetter
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from .env file
load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--task", default="output 'hello world'")
parser.add_argument("--language", default="python")
args = parser.parse_args()

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
api_key = os.environ["API_KEY"]

chat = AzureChatOpenAI(
    api_key=api_key,
    azure_deployment=deployment,
    api_version="2024-02-01",
)

system_prompt = "You will only give the code snippet."
code_prompt = PromptTemplate.from_template(
    "{system_prompt}\nWrite a very short {language} function that will {task}."
)
test_prompt = PromptTemplate.from_template(
    "{system_prompt}\nWrite a test for the following {language} code:\n{code}"
)

code_chain = code_prompt | chat | StrOutputParser() | {"code": RunnablePassthrough()}
test_chain = (
    {
        "code": itemgetter("code"),
        "language": itemgetter("language"),
        "system_prompt": itemgetter("system_prompt"),
    }
    | test_prompt
    | chat
    | StrOutputParser()
)

# Step 1: Invoke the code_chain
code_result = code_chain.invoke(
    {
        "system_prompt": system_prompt,
        "task": args.task,
        "language": args.language,
    }
)

# Step 2: Print the output of the first chain
print("Generated Code>>>>>>\n", code_result["code"])

# Step 3: Use the result of the first chain in the test_chain
result = test_chain.invoke(
    {
        "system_prompt": system_prompt,
        "language": "python",
        "code": code_result["code"],
    }
)

print("Test Code:>>>>>\n", result)

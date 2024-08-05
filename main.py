from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
deployment = os.environ.get("CHAT_COMPLETIONS_DEPLOYMENT_NAME")
api_key = os.environ.get("API_KEY")

embeddings = AzureOpenAIEmbeddings(
    openai_api_key=api_key,
    openai_api_type="azure",
    azure_endpoint=endpoint,
    openai_api_version="2024-02-01",
    model="text-embedding-ada-002",
)
DB_PERSIST_DIRECTORY = "emb_db"


def seed():

    if not os.path.exists(DB_PERSIST_DIRECTORY):
        text_splitter = CharacterTextSplitter(
            separator="\n", chunk_size=200, chunk_overlap=0
        )

        loader = TextLoader("facts.txt")
        docs = loader.load_and_split(text_splitter=text_splitter)

        db = Chroma.from_documents(
            docs, embedding=embeddings, persist_directory=DB_PERSIST_DIRECTORY
        )

        # test the db
        results = db.similarity_search("Where is the largest railway networks?")

        for result in results:
            print("\n")
            print(result.page_content)

    print("Successfully Seeded!")


if __name__ == "__main__":
    seed()

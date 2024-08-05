# Code Generation and Testing with Azure OpenAI

This repository contains a Python script that utilizes the Azure OpenAI service to generate a code snippet based on a given task and then generates a corresponding test for that code. The script uses the `langchain-openai` library to interact with Azure OpenAI and follows a chain of prompts to achieve the desired output.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.10 or higher
- `python-dotenv`
- `langchain-openai`

You will also need access to Azure OpenAI service with the appropriate API keys and deployment details.

## Setup

1. Clone the repository.
2. Create a `.env` file in the root directory and add your Azure OpenAI credentials:

    ```env
    AZURE_OPENAI_ENDPOINT=<your_azure_openai_endpoint>
    CHAT_COMPLETIONS_DEPLOYMENT_NAME=<your_deployment_name>
    API_KEY=<your_api_key>
    ```

3. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

The script can be run from the command line with customizable task and language parameters.

```sh
python script.py --task "Generate a list of integers" --language "python"
```
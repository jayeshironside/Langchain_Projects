import os
from dotenv import load_dotenv
# Use the environment variables to retrieve API keys
load_dotenv()
HUGGINGFACEHUB_API_KEY = os.getenv("HUGGINGFACEHUB_API_KEY")

from langchain.llms import HuggingFaceHub

# repo_id = "google/flan-t5-xxl"
# repo_id = "databricks/dolly-v2-3b"
# repo_id = "databricks/dolly-v2-12b"
repo_id = "meta-llama/Llama-2-13b"

# Initialize Hugging Face LLM without the api_key parameter
llm_huggingface = HuggingFaceHub(repo_id=repo_id, model_kwargs={"temperature": 0.9, "max_length": 64})

our_query = "Describe about mahendra singh dhoni?"
completion_huggingface = llm_huggingface(our_query)
print(completion_huggingface)

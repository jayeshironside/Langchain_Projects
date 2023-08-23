import os
from dotenv import load_dotenv
# Use the environment variables to retrieve API keys
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACEHUB_API_KEY = os.getenv("HUGGINGFACEHUB_API_KEY")

import re
import requests
import openai
import pinecone
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

# LOAD DOCUMENTS - Loads the pdf files available in a directory with pypdf
def load_docs(directory):
    loader = PyPDFDirectoryLoader(directory)
    documents = loader.load()
    return documents

# passing the directory to the 'load_docs' function
directory = 'Docs/'
documents = load_docs(directory)
print(len(documents))

# TRANSFORM DOCUMENTS - Split the document into smaller chunks
def split_docs(documents, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(documents)
    return docs

docs = split_docs(documents)
print(len(docs))

# GENERATE TEXT EMBEDDINGS - OpenAi LLM for creating Embeddings for document/text
# embeddings = OpenAIEmbeddings(model_name="ada")
#       (OR)          We can use any of these models
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# VECTOR STORE - using Pinecone as a vectordb
pinecone.init(
    api_key="c94ef138-be79-47a2-b0ce-08188a79678b",
    environment="gcp-starter"
 )

index_name = "mcq-creators" #Provide the name of index which was created on pinecone
index = Pinecone.from_documents(docs, embeddings, index_name=index_name)

# RETRIEVE ANSWERS
def get_similar_docs(query, k=2):
    similar_docs = index.similarity_search(query, k=k)
    return similar_docs

llm = HuggingFaceHub(repo_id="bigscience/bloom", model_kwargs={"temperature":1e-10})
llm

chain = load_qa_chain(llm, chain_type="stuff")

def get_answer(query):
    relevant_docs = get_similar_docs(query)
    print(relevant_docs)
    response = chain.run(input_documents=relevant_docs, question=query)
    return response

our_query = "Who is Naval Ravikant?"
answer = get_answer(our_query)
print(answer)

# STRUCTURE THE OUTPUT
response_schemas = [
    ResponseSchema(name="question", description="Question generated from provided input text data."),
    ResponseSchema(name="choices", description="Available options for a multiple-choice question in comma separated."),
    ResponseSchema(name="answer", description="Correct answer for the asked question.")
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# This helps us fetch the instruction the langchain creates to fetch the response in desired format
format_instructions = output_parser.get_format_instructions()

# Create chatgpt object
chat_model = ChatOpenAI()

# Prompt Template
prompt = ChatPromptTemplate(
    messages=[
        HumanMessagePromptTemplate.from_template("""When a text input is given by the user, please generate multiple choice questions 
        from it along with the correct answer. 
        \n{format_instructions}\n{user_prompt}""")  
    ],
    input_variables=["user_prompt"],
    partial_variables={"format_instructions": format_instructions}
)

final_query = prompt.format_prompt(user_prompt = answer)
print(final_query)

final_query_output = chat_model(final_query.to_messages())
print(final_query_output.content)

# While with the scenarios like above where we have to process multi-line strings ('\n') in such situations we use re.DOTALL
# Extract json data from the markdown text that we have

markdown_text = final_query_output.content
json_string = re.search(r'{(.*?)}', markdown_text, re.DOTALL).group(1)
print(json_string)
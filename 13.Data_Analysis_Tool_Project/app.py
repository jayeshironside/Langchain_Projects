import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

import streamlit as st
from utils import query_agent

st.set_page_config(page_title="Data Analysis Tool", page_icon="☯")
st.title("Let's do some analysis on your CSV..")
st.header("Please upload your CSV file here:")

# Capture the CSV file
data = st.file_uploader("Upload CSV file", type="csv")

user_message = st.chat_input(placeholder="Enter your query...")

if user_message:
    answer = query_agent(data, user_message)
    st.write(answer)
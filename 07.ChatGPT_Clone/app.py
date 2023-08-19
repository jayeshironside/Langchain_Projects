import os
from dotenv import load_dotenv
# Use the environment variables to retrieve API keys
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

import streamlit as st
from streamlit_chat import message
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory, 
                                                  ConversationSummaryMemory, 
                                                  ConversationBufferWindowMemory
                                                  )
from langchain.memory import ConversationTokenBufferMemory

# Setting page title and header
st.set_page_config(page_title="Chat GPT Clone", page_icon="🤖")
st.markdown("<h1 style='text-align: centre;'>How can i assist you ?</h1>", unsafe_allow_html=True)

st.sidebar.title("😎")
api_key = st.sidebar.text_input("What's your API key?", type="password")
summarize_button = st.sidebar.button("Summarise the conversation", key="summarise")
if summarize_button:
    summarise_placeholder = st.sidebar.write("Nice chatting with you my friend ♥: \n\n"+"Hello Friend")
    summarise_placeholder.write("Nice chatting with you my friend ♥: \n\n"+st.session_state['conversation'].memory.buffer)

# llm = OpenAI(temperature=0, model_name='text-davinci-003')  #we can also use 'gpt-3.5-turbo'
# conversation = ConversationChain(llm=llm, verbose=True, memory=ConversationBufferMemory())

# print(conversation.predict(input="Good Morning AI !"))
# print(conversation.predict(input="My name is Jayesh"))
# print(conversation.predict(input="I stay in Ahmedabad, India"))
# print(conversation.memory.buffer)
# print(conversation.predict(input="What is my name?"))

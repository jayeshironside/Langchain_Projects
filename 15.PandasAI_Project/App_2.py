# Import Libraries
import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import pandas as pd
from pandasai import PandasAI
from pandasai.llm import OpenAI
import matplotlib.pyplot as plt

# API Key retrieval
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Data Analysis Tool", page_icon="🔧", layout="wide")

# Sidebar contents
with st.sidebar:
    st.title('Pandas-AI 🐼')
    st.markdown('''
    ## About
    This app is a data analysis tool created using:
    - ### [Streamlit](https://streamlit.io/)
    - ### [Pandas](https://pandas.pydata.org/docs/)
    - ### [PandasAI](https://github.com/gventuri/pandas-ai)
    - ### [OpenAI LLM model](https://platform.openai.com/docs/models)
    ''')
    add_vertical_space(20)
    st.write('Made with ❤️ by [Jayesh_Ironside](https://github.com/jayeshironside)')

# Front-end and Back-end starts here
st.title("Prompt-driven analysis tool 🔧")

st.session_state.df = None

if st.session_state.df is None:
        uploaded_file = st.file_uploader("Upload a CSV file for analysis", type=['csv'])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df

if st.session_state.df is not None:
    st.subheader("Current dataframe:")
    st.write(st.session_state.df.head(5))
    st.write("Rows x Column :", df.shape)

with st.form("Question"):
        question = st.text_input("Question", value="", type="default")
        submitted = st.form_submit_button("Submit")
        if submitted:
            with st.spinner("Generating you response..."):
                llm = OpenAI(api_token=OPENAI_API_KEY)
                pandas_ai = PandasAI(llm, verbose=True)
                x = pandas_ai.run(df, prompt=question)

                fig = plt.gcf()
                if fig.get_axes():
                    st.pyplot(fig)
                st.write("👉 Generated Response :", x)
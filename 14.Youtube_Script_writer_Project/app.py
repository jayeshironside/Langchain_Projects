import streamlit as st
from utils import generate_script
import time

st.set_page_config(page_title="Script Writer", page_icon="📝")

# Applying styling
st.markdown("""
<style>
div.stButton > button:first-child{
            background-color: #0099ff;
            color: #ffffff;
}
div.stButton > button:hover{
            background-color: #00ff00;
            color: #000000;
}
</style>""", unsafe_allow_html=True)

# Creating session state variable
if 'API_Key' not in st.session_state:
    st.session_state['API_Key'] = ''

# st.title('❤ Youtube script writing tool')

# Sidebar
st.sidebar.image('./logo.png', width=300, use_column_width=True)
st.sidebar.divider()
st.sidebar.title("A Youtube script writer 🖊")

# Capture user inputs
prompt = st.sidebar.text_input(label='Video Title 📃', key="prompt", placeholder='Please provide the topic of the video')
st.sidebar.write("")
video_length = st.sidebar.text_input(label='Video length ⏰', key="video_length", placeholder='Expected video length In minutes')
st.sidebar.write("")
creativity = st.sidebar.slider('Creativity 💭 - (0 Low || High 1)', 0.0, 1.0, 0.2, step=0.1)
st.sidebar.write("")
submit = st.sidebar.button("Generate script for me")
st.sidebar.divider()
st.sidebar.info('The script is generated using Ai models.', icon="ℹ️")

st.title("A Youtube script writer 🖊")
if submit:
    search_result,title,script = generate_script(prompt, video_length, creativity)
    st.success('Hope you like this script 🧡')

    #Display title
    st.subheader('Title: 🔥')
    st.write(title)

    #Display video script
    st.subheader('Your video script: 📃')
    st.write(script)

    #Display the search engine result
    st.subheader("Check Out - DuckDuckGo search:🔍")
    with st.expander('Show me 👀'):
        st.info(search_result)
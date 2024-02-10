import openai
import streamlit as st
from PIL import Image
from streamlit_extras.let_it_rain import rain 
from streamlit_option_menu import option_menu
from gtts import gTTS
import IPython.display as ipd
import os

img  = Image.open('Blue.png')
st.set_page_config(page_title='CHAT WITH BLUE', page_icon=img)

hide_main_style = """ 
        <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        </style>
"""

st.markdown(hide_main_style, unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Bot","Notes","Contact"],
        icons=["robot","bell fill","telephone"],
        menu_icon=None, 
        default_index=0,
    )

if selected == "Notes":
    st.markdown("▸ By utilizing the OpenAI API key, I can help you take advantage of cutting-edge natural language processing technology. This will allow your application to analyze and generate text with remarkable accuracy and speed. The OpenAI API key provides access to a wide range of AI-powered language models that can be trained to perform various tasks such as language translation, sentiment analysis, and question-answering. 

In addition to text analysis, I can also implement TTS (Text-to-Speech) functionality in your application. This feature will enable your users to listen to the generated text in a more natural and human-like voice. TTS technology uses advanced algorithms to convert written text into spoken words, which can be particularly useful for people with visual impairments or reading difficulties.

Finally, I can create a user-friendly GUI (Graphical User Interface) that will make it easy for your users to interact with your application and access its features. The GUI can be designed to match your brand's look and feel and can include various widgets such as buttons, menus, and forms. This will provide your users with a seamless and intuitive experience.") 
    st.markdown("Check out my github:")
    st.link_button("GitHub","https://github.com/Sadhurahavan5555")

if selected == "Contact":
    st.markdown("Gmail")
    st.markdown("sadhurahavan07@gmail.com")

if selected == "Bot":

    st.title("CHAT WITH BLUE👋")
    user_message = "👤"
    name = "🤖"

    openai.api_key = st.secrets["API_KEY"]

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"  

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type Here"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message(user_message):
            st.markdown(prompt)

        with st.spinner(text="Thinking..."):
            response = openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )

        full_response = response.choices[0].message["content"].strip()

        with st.chat_message("assistant"):
            st.markdown(full_response)

            tts = gTTS(full_response, lang='en')
            audio_file = f'assistant_response_{len(st.session_state.messages)}.mp3'
            tts.save(audio_file)

            st.audio(audio_file, format='audio/mp3', start_time=0)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

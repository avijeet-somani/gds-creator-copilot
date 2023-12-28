import streamlit as st
import gemini_model
from gemini_model import KlayoutCopilot_Gemini
#from html_template import css, bot_template, user_template
import subprocess

@st.cache_resource
def load_model() : 
    print('load model')
    gemini = KlayoutCopilot_Gemini()
    return gemini

@st.cache_resource
def write_welcome_message():
    print('write_welocome_message')
    with st.chat_message("assitant") :
        message = st.session_state.conversation.chat.history[1]
        st.markdown(message.parts[0].text)


def display_all_messages() : 
    for index, message in enumerate(st.session_state.conversation.chat.history):
        if index <= 1 : 
           continue;
        if index % 1 : #assistant
           with st.chat_message("assitant") :   
               st.write(message.parts[0].text)  
        else : #user
            with st.chat_message("user") :   
               st.markdown(message.parts[0].text)  



def handle_userinput(user_question=None):
    print('handle_userinput')
    #response = st.session_state.conversation({'question': user_question})
    if user_question : 
        response = st.session_state.conversation.get_response(user_question)
        #display_all_messages()
        
        with st.chat_message("user"):
            st.markdown(user_question)
        with st.chat_message("assitant") :
            st.write(response)
        

st.title("GDS Copilot")
model = load_model()   


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation" not in st.session_state: 
    st.session_state.conversation = model

# Display chat messages from history on app rerun


write_welcome_message()


user_input = st.chat_input("Your Message")
if user_input : 
    handle_userinput(user_input)



import streamlit as st
import openai
import os
# Set up the page layout
st.set_page_config(page_title="P-Tutor", page_icon="pixel_pencil.png", layout='wide')

# Function to display chat messages
def display_chat_message(role, content,avatar):
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)

def display_intro():
    st.title("Plug's Python Tutor")
    st.write('Sheeeee')

daniel = "https://raw.githubusercontent.com/Madlittledude/Brain_Storm/main/isaiah.png"
padty = "https://raw.githubusercontent.com/Madlittledude/Brain_Storm/main/Madlittledude 2_white.png"
def display_chat_interface():

    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        avatar = padty if message["role"] == "assistant" else daniel
        display_chat_message(message["role"], message["content"],avatar)

    # User input
    prompt = st.chat_input("Start thinking with your fingers...get your thoughts out")
    if prompt:
        # Set the state to indicate the user has sent their first message
        st.session_state.first_message_sent = True
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_chat_message("user", prompt,daniel)

        with st.chat_message("assistant",avatar=padty):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=([
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]),
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


# Initialization logic
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": ('''You are Isaiah (The Pluuug)'s private tutor for python and life in general. He is a beginner, 
            so he will need you to help him articulate his ideas.I need you to do the following:  
            Do not give him complete code unless he asks for it explicitly.
            Help him break down and articulate his idea. Enlighten him to tips and tricks with python as your go. Lastly, encourage him to never give up. Time is of the essence.'''
                        )
                    }]



if "first_message_sent" not in st.session_state:
    st.session_state.first_message_sent = False

openai.api_key = os.environ["OPENAI_API_KEY"]

# Display logic
if not st.session_state.first_message_sent:
    display_intro()

display_chat_interface()






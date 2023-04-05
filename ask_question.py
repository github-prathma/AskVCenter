import streamlit as st

def askQuestion():

    # Add a text input box for the user's question
    user_question = st.text_input(
        "Enter Your Developer Question: ",
        placeholder = "Your AI assistant here! Ask me anything...")
    return user_question


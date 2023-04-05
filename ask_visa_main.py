import streamlit as st
from load_model import *
from ask_question import *
import logging

tone = 'formal'
persona = 'buddha'

if "generated" not in st.session_state:
    # generated output
    st.session_state["generated"] = [] 
if "past" not in st.session_state:
    # past input
    st.session_state["past"] = []
if "input" not in st.session_state:
    # user question current
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    # conversation memory provides
    st.session_state["stored_session"] = []


st.title("✅ Ask Visa Developer")

API = st.sidebar.text_input(
    "API-Key",
    placeholder = "**************************",
    type="password"
)

MODEL = st.sidebar.selectbox(label='Model', options=['gpt-3.5-turbo', 'text-davinci-003', 'text-davinci-002', 'code-davinci-002'])


# If an API key has been provided, create an OpenAI language model instance
if API:
    llm = getModel(API, MODEL)
    chain = getQAChain(llm)
    docsearch = getDocSearchFromData(API)
    user_input = askQuestion()

    if user_input:
        documents = docsearch.similarity_search(user_input, include_metadata=True)
        output = chain(
                {
                    "input_documents": documents,
                    "human_input": user_input,
                    "tone": tone,
                    "persona": persona,
                },
                return_only_outputs=True,
            )["output_text"]
        st.session_state["past"].append(user_input)
        st.session_state["generated"].append(output)

    with st.expander("Chat with AI Assistant"):
        for i in range(len(st.session_state["generated"])):
            st.info(st.session_state["past"][i])
            st.success(st.session_state["generated"][i])
else:
    # If an API key hasn't been provided, display a warning message
    st.warning("Enter your OPENAI API-KEY. Get your OpenAI API key from [here](https://platform.openai.com/account/api-keys).\n")




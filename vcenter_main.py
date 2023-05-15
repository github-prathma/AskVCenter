import streamlit as st
from load_model import *
from ask_question import *
import logging
from constants import ask_category

tone = 'formal'
persona = 'buddha'

if "generated_dev" not in st.session_state:
    # generated output (dev center)
    st.session_state["generated_dev"] = [] 
if "generated_business" not in st.session_state:
    # generated output (business next gen commerce)
    st.session_state["generated_business"] = [] 
if "generated_support" not in st.session_state:
    # generated output (support FAQ)
    st.session_state["generated_support"] = [] 
if "past_dev" not in st.session_state:
    # past input (dev center)
    st.session_state["past_dev"] = []
if "past_business" not in st.session_state:
    # past input (business next gen commerce)
    st.session_state["past_business"] = []
if "past_support" not in st.session_state:
     # past input (support FAQ)
    st.session_state["past_support"] = []
if "input" not in st.session_state:
    # user question current
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    # conversation memory provides
    st.session_state["stored_session"] = []

def session_for_category(category):
    logging.info("category selected: " + CATEGORY)
    past = ""
    generated = ""
    if category == ask_category.AskCategory.DEV_CENTER.value:
        past = "past_dev"
        generated = "generated_dev"
    elif category == ask_category.AskCategory.BUSINESS_COMM.value:
        past = "past_business"
        generated = "generated_business"
    elif category == ask_category.AskCategory.FAQ.value:
        past = "past_support"
        generated = "generated_support"
    return past, generated

def store_session(category, user_input, output):
    past_input, generated_output = session_for_category(category)
    st.session_state[past_input].append(user_input)
    st.session_state[generated_output].append(output)
    
def load_session_state(category):
    past_input, generated_output = session_for_category(category)
    for i in range(len(st.session_state[generated_output])):
        st.info(st.session_state[past_input][i])
        st.success(st.session_state[generated_output][i])

st.title("✅ Ask Visa Developer")

API = st.sidebar.text_input(
    "API-Key",
    placeholder = "**************************",
    type="password"
)

MODEL = st.sidebar.selectbox(label='Model', options=['gpt-3.5-turbo', 'text-davinci-003', 'text-davinci-002', 'code-davinci-002'])

CATEGORY = st.sidebar.selectbox(label='Ask About', options=[e.value for e in ask_category.AskCategory])

# If an API key has been provided, create an OpenAI language model instance
if API:
    llm = getModel(API, MODEL)
    chain = getQAChain(llm)
    createAndSaveEmbeddingsPickle(API)

    if CATEGORY: 
        docsearch = getDocSearchForCategory(CATEGORY)
        user_input = askQuestion()

        if user_input:
            documents = docsearch.similarity_search(user_input, include_metadata=True)
            output = chain(
                    {
                        "input_documents": documents,
                        "human_input": user_input,
                        "tone": tone,
                        "persona": persona,
                        "category": CATEGORY
                    },
                    return_only_outputs=True,
                )["output_text"]
            store_session(CATEGORY, user_input, output)

        with st.expander("Chat with AI Assistant"):
            load_session_state(CATEGORY)
    else:
        # If an API key hasn't been provided, display a warning message
        st.error("Please choose category to proceed!!\n")

else:
    # If an API key hasn't been provided, display a warning message
    st.warning("Enter your OPENAI API-KEY. Get your OpenAI API key from [here](https://platform.openai.com/account/api-keys).\n")

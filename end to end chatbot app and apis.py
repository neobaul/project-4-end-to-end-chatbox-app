# load libraries
import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# load environment variables from .env file
load_dotenv()

# set page configuration for streamlit app
st.set_page_config(
    page_title="Enhanced QA Chatbot with OpenAI",
    page_icon="🤖",
    layout="wide"
)

# title of the app
st.title("Enhanced QA Chatbot with OpenAI")
st.markdown(
    """
    This is an enhanced question-answering chatbot built using OpenAI's API and Streamlit. 
    It can handle complex queries and provide detailed responses.
    """
)

# settings for sidebar
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input(
        "Enter your OpenAI API Key", 
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        help="You can find your API key in your OpenAI account settings. from https://platform.openai.com/account/api-keys"
    )

    # openai model selection
    engine = st.selectbox(
        "Select OpenAI Model",
        options=["gpt-3.5-turbo", "gpt-4", "gpt-4-32k", "gpt-5.5 Pro"],
        index=0,
        help="Choose the OpenAI model for generating responses. GPT-4 or GPT-5.5 Pro is more powerful but may have higher latency and cost."
    )

# response parameters
    temperature = st.slider(
        "Response Creativity (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher values (e.g., 0.8) make the output more creative, while lower values (e.g., 0.2) make it more focused and deterministic."
    )

    max_tokens = st.slider(
        "Maximum Response Length (Tokens)",
        min_value=50,
        max_value=2000,
        value=500,
        step=50,
        help="Maximum number of tokens for the generated response."
        )

# prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Please provide clear, concise responses to user queries."),
    ("user", "Question: {question}")
])

def generate_response(question, api_key, model, temperature, max_tokens):
    try: 
        llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )

        chain = prompt | llm | StrOutputParser() 
        response = chain.invoke({"question": question})
        return response
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None
    
# main chat interface
st.subheader("Chat with the AI")
user_input = st.chat_input("Enter your question here...")

if user_input:
    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar to continue.")
        st.stop()

    with st.spinner("Generating response..."):
        response = generate_response(
            question=user_input,
            api_key=api_key,
            model=engine,
            temperature=temperature,
            max_tokens=max_tokens
        )
    if response:
        # display the AI response
        with st.chat_message("user"):
            st.write(f"**You:** {user_input}")
        with st.chat_message("assistant"):
            st.write(f"**AI:** {response}")
    else:
        st.error("Failed to generate response. Please check your API key and try again.")

# add some helpful info
st.markdown(
    """
    ---
    **Tips for Best Results:**
    - Be specific with your questions
    - For complex topics, break them into smaller questions
    - Adjust temperature for more creative or more focused answers.
    """
)
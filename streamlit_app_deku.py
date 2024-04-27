import openai
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI, OpenAI
import pandas as pd
import getpass
import os
import streamlit as st
from pydantic import ValidationError

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def create_agent(csv_file):
    try:

        return create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
        csv_file,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        )
     except ValidationError as e:
        print("Validation errors:", e.errors())  # Log the specific errors
        raise e

def upload_file():
    file_path = st.file_uploader("Choose a CSV file", type="csv")
    if file_path:  # Ensure a file was selected
        global agent  # Declare agent as a global variable to use it later
        agent = create_agent(file_path)  # Initialize agent with the uploaded file
        st.write("File uploaded and agent created. Ask your questions!")
    else:
        st.write("No file selected. Please try again.")

def ask_question(question):
    if not question:
        st.write("Please enter a question.")
    elif not hasattr(agent, 'run'):
        st.write("Please upload a file first.")
    else:
        try:
            reply = agent.run(question)
            st.write(f"Reply: {reply}")
        except Exception as e:
            st.write(f"Error: {e}")

upload_file()

question = st.text_input("Enter your question here:")
ask_question(question)
# Conversational AI Chatbot with Google Gemini API

This project is a Streamlit-based chatbot that interacts with users to collect specific details such as name, place of birth, university, email, and field of study. The chatbot uses the Google Gemini API to extract and validate these details from user input.

# Demo
View the [demo](https://drive.google.com/file/d/1N58wfS3-mvZsaCiH7Gyuujx7nhv4Kq6u/view?usp=drive_link).

## Features

- **Conversational Interface**: The chatbot engages users in a conversation to collect specific personal details.
- **Dynamic Prompting**: Asks users for missing details based on the conversation.
- **Google Gemini API Integration**: Utilizes the Gemini API to extract and parse information from user input.
- **Session Management**: Tracks details and conversation state across multiple user interactions.
- **Chat History**: Saves and displays the chat history during the session.

### Prerequisites

- Python 3.7 or higher
- `pip` package manager
- A Google Gemini API key
- Environment variables set for API key

## Install Dependencies:

Install the required Python packages using pip:
pip install -r requirements.txt

## Set Up Environment Variables:
Create a .env file in the root directory and add your Google Gemini API key:
GOOGLE_API_KEY=your_api_key_here
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

## Run the Application:
Start the Streamlit application by running the following command:
streamlit run app.py

### Imports and Environment Setup

import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import shelve

## Save Chat History:

The chat history is automatically saved during the session and can be reviewed later.



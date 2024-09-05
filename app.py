import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import shelve

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# Initialize dictionaries for details and tracking
if "details_dict" not in st.session_state:
    st.session_state.details_dict = {
        "Name": "",
        "Place of Birth": "",
        "University": "",
        "Email": "",
        "Field of Study": ""
    }

if "acquired_details" not in st.session_state:
    st.session_state.acquired_details = {
        "Name": False,
        "Place of Birth": False,
        "University": False,
        "Email": False,
        "Field of Study": False
    }

if "count" not in st.session_state:
    st.session_state.count = 0

details_dict = st.session_state.details_dict
acquired_details = st.session_state.acquired_details
count = st.session_state.count

def get_gemini_response(question):
    try:
        chat = model.start_chat()
        response = chat.send_message(question, stream=True)
        response_text = ""
        for chunk in response:
            response_text += f"{chunk.text}\n"
        return response_text
    except Exception as e:
        print(f"Error getting response from Gemini: {e}")
        return ""

def extract_details(text):
    prompt = (
        f"Extract the following details from the user input: 'Name', 'Place of Birth', 'University', 'Email', and 'Field of Study'. "
        f"Return 'not found' for any field that is not present in the user input. "
        f"Provide the extracted information in a clear and organized manner. "
        f"User Input: {text}"
    )    
    response_text = get_gemini_response(prompt)
    return response_text

def parse_details(text):
    details = {
        "Name": "Not found",
        "Place of Birth": "Not found",
        "University": "Not found",
        "Email": "Not found",
        "Field of Study": "Not found"
    }

    for line in text.splitlines():
        for key in details:
            if key in line:
                details[key] = line.split(":")[-1].strip()
    return details

def update_details(key, value):
    details_dict[key] = value
    acquired_details[key] = True

def get_conversational_prompt(missing_details, text):
    if "Name" in missing_details:
        prompt = (
            "Create a polite and engaging response to ask the user for their name. "
            "The response should encourage the user to share their name."
        )
        response_text = get_gemini_response(prompt)
        return response_text
    elif "Place of Birth" in missing_details:
        prompt = (
            f"Create a polite and engaging response to ask the user for their place of birth. "
            f"Mention their name {details_dict['Name']} if available. "
            "The response should encourage the user to share this information."
        )
        response_text = get_gemini_response(prompt)
        return response_text
    elif "University" in missing_details:
        prompt = (
            f"Create a polite and engaging response to ask the user for the university or college "
            f"they are studying at or have graduated from. Mention their name {details_dict['Name']} "
            f"if available. The response should encourage the user to share this information."
        )
        response_text = get_gemini_response(prompt)
        return response_text
    elif "Email" in missing_details:
        prompt = (
            f"Create a polite and engaging response addressing the user with their name {details_dict['Name']} to ask for their email address. "
            "The response should encourage the user to share their email."
        )
        response_text = get_gemini_response(prompt)
        return response_text
    elif "Field of Study" in missing_details:
        prompt = (
            f"Create a polite and engaging response addressing the user with their name {details_dict['Name']} to ask for their field of study or branch. "
            "The response should encourage the user to share this information."
        )
        response_text = get_gemini_response(prompt)
        return response_text
    else:
        return "Is there anything else you’d like to share with me?"

def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input from user
if prompt := st.chat_input("What is up?", key="initial_input"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Extract details using Gemini
    response_text = extract_details(prompt)
    details = parse_details(response_text)
    
    # Update the extracted details
    for key, value in details.items():
        val = value.strip().lower()  # Strip whitespace and convert to lowercase
        if "not" not in val and val != '':  # Correct the condition logic
            update_details(key, value)
    response = ""
    # Ask for missing details if any
    if not all(acquired_details.values()):
        missing_details = [key for key, acquired in acquired_details.items() if not acquired]
        if missing_details:
            follow_up_prompt = get_conversational_prompt(missing_details, prompt)
            response = follow_up_prompt
    
    # Display the assistant's final message
    with st.chat_message("assistant"):
        st.markdown(response)
        if prompt.lower() == "yes" and response == "":
                response="All details are collected. Can you provide feedback?"
                st.markdown(response)
                st.session_state.count += 1
        else:
            if count >= 1:
                response="Thank you for providing the Feedback!"
                st.markdown(response)
            else:
                
                if all(acquired_details.values()):
                    response="Thank you for providing all the information!\nHere's what I have gathered:\n"
                    st.markdown(response)
                    for key, value in details_dict.items():
                        st.markdown(f"**{key}:** {value}")
                        response += f"**{key}:** {value}\n"
                    response += "If everything looks good, please confirm with YES, or let me know if there's anything you'd like to change."
                    st.markdown("If everything looks good, please confirm with YES, or let me know if there's anything you'd like to change.")
    st.session_state.messages.append({"role": "assistant", "content": response})

save_chat_history(st.session_state.messages)

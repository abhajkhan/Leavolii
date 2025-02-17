import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

initial_message = [
    {"role": "system", "content": "You are a Leave Letter writing assistant at Malabar College of Advanced Studies, Vengara. You are helping students to write a leave letter to the Tutor of the student's class. Ask the student their name, department, Year/Semester, name of the Tutor, the reason for leave, days in which requesting leave and all other neccessary details step by step. Finally, generate the personalized leave letter for the student."},
    {"role": "assistant", "content": "Hello, I'm at your service. Please provide me with the following details to generate a leave letter for you."},
]


def get_response_from_llm(messages):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return "Sorry, I encountered an error. Please try again."


if "messages" not in st.session_state:
    st.session_state.messages = initial_message

st.title("Leavolii")

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

user_message = st.chat_input("Say something!")
if user_message:
    new_message = {"role": "user", "content": user_message}
    st.session_state.messages.append(new_message)

    with st.chat_message("user"):
        st.markdown(user_message)

    response = get_response_from_llm(st.session_state.messages)

    if response:
        response_message = {"role": "assistant", "content": response}
        st.session_state.messages.append(response_message)

        with st.chat_message("assistant"):
            st.markdown(response)

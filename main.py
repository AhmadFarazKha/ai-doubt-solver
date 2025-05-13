import streamlit as st
from utils import ask_question

# Streamlit Page Setup
st.set_page_config(page_title="AI Doubt Solver", layout="centered")

# Title
st.title("🎓 AI-Powered Educational Doubt Solver")

# Input from User
query = st.text_input("Ask your academic question (any subject, any topic):")

# If user clicks the button
if st.button("Get Answer"):
    if query.strip() == "":
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Thinking..."):
            answer = ask_question(query)
            st.success("Here's your answer:")
            st.write(answer)

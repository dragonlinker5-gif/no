import streamlit as st

st.title(" Prototype Sandbox")
st.write("Welcome to the control center. System online.")

# A quick interactive element to test that it works
user_input = st.text_input("Enter a chaotic idea:")
if user_input:
    st.write(f"Analyzing logical frameworks for: {user_input}")

import streamlit as st
from agent import call_agent

def main():
    """_summary_
    """
# Streamlit app
    st.title("Bedtime Story Generator")

    # User input
    story_topic = st.text_input("Enter a topic for your bedtime story:")

    # Button to trigger the agent
    if st.button("Generate Story"):
        if story_topic:
            response = call_agent(story_topic)
            st.success(response)
        else:
            st.warning("Please enter a topic before generating the story.")

if __name__=='__main__':
    main()
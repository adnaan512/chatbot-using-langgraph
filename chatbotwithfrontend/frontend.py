import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG_ID = {"configurable": {"thread_id": "1"}}

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

user_input = st.chat_input("Type your message:")

# Display previous chat
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

if user_input:
    # Append user message
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    # Stream AI response
    with st.chat_message("assistant"):
        response_container = st.empty()
        collected_text = ""

        for message_chunk, metadata in chatbot.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=CONFIG_ID,
            stream_mode="messages"
        ):
            collected_text += message_chunk.content
            response_container.markdown(collected_text)

    # Store assistant message
    st.session_state["message_history"].append({"role": "assistant", "content": collected_text})

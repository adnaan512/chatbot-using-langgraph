import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []
input=st.chat_input("Type your message:")
for message in st.session_state["message_history"]:
   with st.chat_message(message["role"]):
       st.text(message["content"])
if input:
    st.session_state["message_history"].append({"role": "user", "content": input})
    with st.chat_message("user"):
        st.text(input)
    chat_response = chatbot.invoke({"messages": [HumanMessage(content=input)]})
    ai_message = chat_response["messages"][-1].content
    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})
    with st.chat_message("assistant"):
      st.text(ai_message)


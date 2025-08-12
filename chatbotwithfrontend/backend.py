from langgraph.graph import StateGraph,START, END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage ,HumanMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
import os
load_dotenv()
from langgraph.graph.message import add_messages
class chatsate(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

llm=ChatGroq(model="llama-3.3-70b-versatile",api_key=os.environ["GROQ_API_KEY"] )
def chat_node(state:chatsate):
    messages=state["messages"]
    response=llm.invoke(input=messages)
    return {"messages": [response]}
checkpointer=MemorySaver()
graph=StateGraph(chatsate)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)
chatbot=graph.compile(checkpointer=checkpointer)
# thread_id="1"
# while True:
#     user_input = input("type your message: ")
#     if user_input.strip().lower() in ["exit", "quit", "bye"]:
#         break
#     config={"configurable" :{"thread_id": thread_id}}
#     response = chatbot.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)
#     print(response["messages"][-1].content)  # Print the response from the chatbot

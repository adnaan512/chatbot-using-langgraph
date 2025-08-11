from langgraph.graph import StateGraph,START, END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage ,HumanMessage
from langchain_groq import ChatGroq
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
graph=StateGraph(chatsate)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)
chatbot=graph.compile()
intialstate={
    "messages": [HumanMessage(content="Hello, how are you?")]
}
res=chatbot.invoke(intialstate)
print(res)
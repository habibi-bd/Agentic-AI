import os
import operator
import streamlit as st
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Literal

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    BaseMessage,
)
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

 
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    
)


# messages = [
#      SystemMessage(content="You are a helpful assistant writing details for any query."),
#     HumanMessage(content="How to print hello world in java?")
# ]
# ai_msg = llm.invoke(messages)


# class ChatState(TypedDict):
#     messages: Annotated[list[BaseMessage], add_messages]

# def chat_node(state: ChatState):
#     messages = state['messages']
#     response = llm.invoke(messages)
#     return {"messages": [response]}

# # Checkpointer
# checkpointer = InMemorySaver()

# graph = StateGraph(ChatState)
# graph.add_node("chat_node", chat_node)
# graph.add_edge(START, "chat_node")
# graph.add_edge("chat_node", END)

# chatbot = graph.compile(checkpointer=checkpointer)

 
st.set_page_config(page_title="LangGraph Chatbot", page_icon="💬")
st.title("💬 LangGraph Chatbot (Streaming + Separate Backend)")

 

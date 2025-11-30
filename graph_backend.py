from dotenv import load_dotenv
import os

from langgraph.graph import StateGraph,START, END
from typing import TypedDict, Literal, Annotated
from langchain_core.messages import SystemMessage, HumanMessage
import operator
from google import genai

from langchain_google_genai import ChatGoogleGenerativeAI

# -----------------------------
# Define chat state
# -----------------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# -----------------------------
# LLM and chat node
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    
)

def chat_node(state: ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

# -----------------------------
# Graph + Checkpointer
# -----------------------------
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)
chatbot = graph.compile(checkpointer=checkpointer)

# -----------------------------
# Helper functions for Streamlit
# -----------------------------
def get_new_thread_id():
    """Generate a unique thread ID"""
    return str(uuid.uuid4())

def stream_response(user_input: str, thread_id: str):
    """Stream chatbot response token by token"""
    config = {"configurable": {"thread_id": thread_id}}
    for chunk in chatbot.stream({"messages": [HumanMessage(content=user_input)]}, config=config):
        if "messages" in chunk:
            message = chunk["messages"][-1]
            if hasattr(message, "content"):
                yield message.content  # yields each partial token

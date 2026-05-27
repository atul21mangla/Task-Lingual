from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from tools import all_tools
from langchain.agents import create_agent 
from langgraph.checkpoint.memory import InMemorySaver
from database import init_db

load_dotenv()
init_db()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
)

SYSTEM_PROMPT = """You are an intelligent Todo list assistant. 
You help the user manage their tasks in a SQLite database using CRUD tools. 
Always use the search tool if you need to find a task's ID before updating or deleting it.
"""

def get_agent():
    return create_agent(
        model=llm, 
        tools=all_tools, 
        system_prompt=SYSTEM_PROMPT, 
        checkpointer=InMemorySaver()
    )

config = {"configurable":{"thread_id":"thread_1"}}

def run_agent(user_query: str) -> str:
    """Processes natural language query using Groq, determines the right tools to call,
    executes them, and returns a natural language response.
    """
    agent = get_agent()

    res = agent.invoke(
        {"messages":[{"role":"user", "content":user_query}]}, 
        config=config
    )

    return res["messages"][-1].content


if __name__ == "__main__":
    print(run_agent("Add watch IPL Final task for sunday"))
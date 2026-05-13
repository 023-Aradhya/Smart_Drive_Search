from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferWindowMemory
from backend.app.agent import drive_search_tool
from backend.app.prompts import SYSTEM_PROMPT

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

tools = [drive_search_tool]

memory = ConversationBufferWindowMemory(
    k=3,
    memory_key="chat_history",
    return_messages=True
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=False,
    agent_kwargs={
        "system_message": SYSTEM_PROMPT
    }
)
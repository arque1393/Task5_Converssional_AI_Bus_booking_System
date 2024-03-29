from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage, HumanMessage

# Gemini Example 
from langchain_google_genai import ChatGoogleGenerativeAI





from WebApp.elements.llm_tools import create_search_tool, create_math_tools,create_web_search_tools
from WebApp.elements.vector_store import VectorStore

from typing import Annotated


def create_agent_executer(vector_store:VectorStore, name:Annotated[str,'currently suport only Gorq or Gemini']='gorq'):
    search_tool = create_search_tool(vector_store)
    math_tools = create_math_tools()
    web_search_tools = create_web_search_tools()
    if name == 'gorq': 
        from WebApp.elements.llm import gorq_llm as llm
    elif name== 'gemini':
        from WebApp.elements.llm import gemini_llm as llm
    else :
        raise Exception("Currently only gemini or gorq is available")
    
    prompt = hub.pull("hwchase17/structured-chat-agent")

    tools = [search_tool, math_tools, web_search_tools]
    agent = create_structured_chat_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    return agent_executor
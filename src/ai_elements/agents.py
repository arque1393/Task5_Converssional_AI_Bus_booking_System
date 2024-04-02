from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import load_tools
from src.ai_elements.prompts import prompt 
from langchain import hub

# prompt = hub.pull("hwchase17/structured-chat-agent")
# Gemini Example 
from langchain_google_genai import ChatGoogleGenerativeAI



from src.ai_elements.llm import gemini_llm 
from src.ai_elements.llm import gorq_llm 


from src.ai_elements.llm_tools import create_search_tool,create_web_search_tools  ,create_math_tools, create_food_api_tools,create_hotel_api_tools
from src.ai_elements.vector_store import VectorStore

from typing import Annotated


def create_agent_executer(vector_store:VectorStore, name:Annotated[str,'currently support only Gorq or Gemini']='gorq'):
    """Create a Langchain's Agent Executer Object.
    Args:
        vector_store (VectorStore): Custom Vector Store Class that Index documents and store in Vector database.
        name (Annotated[str,&#39;currently support only Gorq or Gemini&#39;], optional): _description_. Defaults to 'gorq'.
    Raises:
        Exception: If input is different from the Gemini and Groq
    Returns:
        _type_: AgentExecutor : Agent executer object to execute Agent 
    """
    search_tool = create_search_tool(vector_store)
    math_tool = create_math_tools()
    web_search_tools = create_web_search_tools()
    food_api_tools = create_food_api_tools()
    hotel_api_tools = create_hotel_api_tools()
    if name == 'gorq': 
        llm = gorq_llm
    elif name== 'gemini':
        llm = gemini_llm
    else :
        raise Exception("Currently only gemini or gorq is available")
    
    tools = load_tools(["llm-math"], llm=llm)

    tools = [search_tool, math_tool, web_search_tools,food_api_tools, hotel_api_tools]
    agent = create_structured_chat_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    return agent_executor
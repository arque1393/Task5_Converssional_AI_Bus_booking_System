from langchain.tools import tool, StructuredTool, Tool
from WebApp.elements.vector_store import VectorStore 
from langchain.chains import LLMMathChain
from langchain_community.tools import DuckDuckGoSearchRun 


from WebApp.elements.llm import gorq_llm

def create_search_tool (vc:VectorStore) -> StructuredTool :
    def knowledge_search(query: str) -> str:
        """Look up things in to knowledge Space."""
        
        docs = vc.similarity_search(query=query,k=5)
        return ' '.join([page.page_content for page in docs]      ) 
    search_tool = StructuredTool.from_function(
        func=knowledge_search,
        name="Knowledge-Space-Explore",
        description="This is Your knowledge base. This is your Primary tool. This is useful for when you need to answer questions.",
    )
    return search_tool

def create_math_tools():
    # calculator tool for arithmetics
    problem_chain = LLMMathChain.from_llm(llm=gorq_llm)
    math_tool = Tool.from_function(name="Calculator", func=problem_chain.run,
                    description="Useful for when you need to answer numeric questions. This tool is only for math questions and nothing else. Only input math expressions, without text",
            )    
    return math_tool
    

def create_web_search_tools():
    search = DuckDuckGoSearchRun()
    Tool.from_function(name="Web Search", func=search.run,
                    description="Useful when you need extra information. Use this tool only when you unable to found answer using Knowledge-Space-Search tools",
                )    
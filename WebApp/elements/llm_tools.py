from langchain.tools import tool, StructuredTool
from WebApp.elements.vector_store import VectorStore 



def create_search_tool (vc:VectorStore) -> StructuredTool :
    def knowledge_search(query: str) -> str:
        """Look up things in to knowledge Space."""
        
        docs = vc.similarity_search(query=query)
        return ' '.join([page.page_content for page in docs]       
       
        
    search_tool = StructuredTool.from_function(
        func=knowledge_search,
        name="Knowledge-Space-Search",
        description="useful for when you need to answer questions",
    )
    return search_tool
    
    
def create_api_call_tool(query:str):
    return f"{query} is search via API Call "
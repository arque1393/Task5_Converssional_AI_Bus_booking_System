from langchain.tools import tool, StructuredTool, Tool
from src.ai_elements.vector_store import VectorStore 
from langchain.chains import LLMMathChain
from langchain_community.tools import DuckDuckGoSearchRun 
import requests
import json
import re
from src.ai_elements.llm import gorq_llm

def create_search_tool (vc:VectorStore) -> StructuredTool :
    def knowledge_search(query: str) -> str:
        """Look up things in to knowledge Space."""
        
        docs = vc.similarity_search(query=query,k=5)
        return ' '.join([page.page_content for page in docs]      ) 
    search_tool = StructuredTool.from_function(
        func=knowledge_search,
        name="Knowledge-Space-Explore",
        description="This is Your knowledge base. This is your Primary tool. This is useful for when you need to answer questions. It only accept query in form of String. Ask question in single line of string.",
    )
    return search_tool

# def create_math_tools():
#     # calculator tool for arithmetics
#     problem_chain = LLMMathChain.from_llm(llm=gorq_llm)
#     math_tool = Tool.from_function(name="Calculator", func=problem_chain.run,
#             description="Useful for when you need to answer numeric questions.Only input math expressions, without text. ",
#         )    
#     return math_tool
def create_math_tools():
    """ return a LLM Tools Python based Math calculator"""
    
    math_tool = Tool.from_function(name="Calculator",
            func=lambda expression : abs(eval(re.sub(r'[^\d.*/\+\-\(\)]', '', expression))),
            description="Useful for when you need to answer numeric questions.Only input math expressions, without text. ",
        )    
    return math_tool

def create_web_search_tools():
    """Use Duck Duck Go Web Search Engine as """
    
    search = DuckDuckGoSearchRun()
    Tool.from_function(name="Web Search", func=search.run,
            description="This is Web Search Tools. Useful when you need extra information or real time data. Use this tool only when you unable to found answer using Knowledge-Space-Search tools",
        )    
    return search


### Food API Tools 
def create_food_api_tools () -> StructuredTool :
    def food_api_tools(query:str):
        url = "https://api.edamam.com/api/food-database/v2/parser"
        params = {"app_id":"5dc0f165", 'app_key':'9134b6acc09d8d3edb2e85e3fc99aa81'}
        headers = {'accept': 'application/json'}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        food_detail = [data['hints'][i]['food'] for i in range(len(data['hints']))]
        for food in food_detail : 
            try: 
                del food['image'] 
            except : 
                pass 
        return food_detail
    
    food_api_tools = StructuredTool.from_function(
        func=food_api_tools,
        name="Food_API_tool",
        description="This Tools provides information related to food",
    )
    return food_api_tools

### Hotel Tools API 
def create_hotel_api_tools () -> StructuredTool :

    def hotel_api_tools(query:str):
        url = "https://booking-com.p.rapidapi.com/v1/hotels/reviews"
        querystring = {"locale":"en-gb","sort_type":"SORT_MOST_RELEVANT","hotel_id":"1676161","customer_type":"solo_traveller,review_category_group_of_friends","language_filter":"en-gb,de,fr"}
        headers = {
            "X-RapidAPI-Key": "e773191cc3msh934be584b0a44afp100dd4jsn0e7b424d8545",
            "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        data =data['result']
        for i in range(len(data)):
            del data[i]['stayed_room_info']
            del data[i]['reviewer_photos']
        return json.dumps(data)
    hotel_api_tools = StructuredTool.from_function(
        func=hotel_api_tools,
        name="Hotel_API_tool",
        description="This Tools provides information related to Hotels.",
    )
    return hotel_api_tools
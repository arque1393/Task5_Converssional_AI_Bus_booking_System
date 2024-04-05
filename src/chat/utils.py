from langchain_core.messages import AIMessage, HumanMessage
import json 
def json_to_chat_history(json_history:list):
    formatted_history= list()
    for i in range(0,len(json_history),2):
        formatted_history.append(HumanMessage.parse_obj(json.loads(json_history[i])))
        formatted_history.append(AIMessage.parse_obj(json.loads(json_history[i+1])))
    
    return formatted_history
        

def chat_history_to_json(chat_history:list):
    formatted_history= [obj.json() for obj in chat_history]    
    return formatted_history
        

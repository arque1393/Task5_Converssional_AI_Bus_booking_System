from langchain_core.messages import AIMessage, HumanMessage

def json_to_chat_history(history:list):
    formatted_history= list()
    for i in range(0,len(history),2):
        formatted_history.append(HumanMessage.parse_obj(history[i]))
        formatted_history.append(AIMessage.parse_obj(history[i+1]))
    
    return formatted_history
        


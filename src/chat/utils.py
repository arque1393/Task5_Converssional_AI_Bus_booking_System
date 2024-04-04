
def parse_chat_history(history:list):
    for i in range(0,len(history),2):
        print(history[i])

if __name__== '__main__':
    parse_chat_history([1,2,3,4,5,6,7,8,9,10])
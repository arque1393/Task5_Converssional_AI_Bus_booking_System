from langchain.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template('''
This is some information for your knoledge:
{knowledge}\n\n
Answer the given question from the previous content.
Question : {question}''')
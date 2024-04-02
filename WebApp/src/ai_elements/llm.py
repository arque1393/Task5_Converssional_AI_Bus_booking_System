from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq


gorq_llm = ChatGroq(temperature=0.5, model_name="mixtral-8x7b-32768")
gemini_llm = ChatGoogleGenerativeAI(model="gemini-pro")
        
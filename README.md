# Task 5 An Intelligent Chat Bot on the specialize domain Bus Booking Service.
 
- **Problem Statement** : A Conversational Chat API  to chat with end users regarding Bus Booking Information 
- **Client Requirements** : 
    An API Backend to chat with a Bot that provide as much as possible accurate information of Bus booking System and can also answers of the relevant questions of th Bus Booking System.

## Creating environment and run Program 
- **Create Environment**
```bash
git clone https://github.com/arque1393/Task5_Converssional_AI_Bus_booking_System.git
cd Task5_Converssional_AI_Bus_booking_System
conda env create -f requirements/base.conda.yml
```
- **Run Project **
```bash
conda activate AI_Assistant
python -m src.main 
```


- **Features** : 
    - An Agent Based System with various LLM Tools.
        - Knowledge Base Search Tools 
        - Mathematics Calculator Tools
        - Api Call Tools 
            - Food API (For Now)
            - Hotel API (For Now )
        - Web Search Tools  (Duck Duck Go Search)
    - Agents can determine the appropriate tools to execute  to find the answer of th query. 
    - Agents can also answer based on previous Chat Reference 

- **Use of LLM Models** 
    - As LLM Model Currently use Gorq LLM. This is the default model of the project 
        - Model Name = "mixtral-8x7b-32768"
    - As a backup also use Google Gemini 
- **Use of Agent**
    - As Agent use Langchan's Structured Chat Agents that works almost perfectly.

- **Required API Keys**
    1. LangSmith API Key for LLM Visualization in LangSmith
        - https://smith.langchain.com/o/e0448a1e-9815-517d-9b65-298b5645922d/settings
    2. Gorq API Key for Using Gorq LLM
        - https://console.groq.com/keys
    3. Google API Key For Gemini 
        - https://aistudio.google.com/app/apikey

- **API End Points**
    - Only Two API end point are available now 
        1. POST  /upload   -> To Upload PDF file in server as knowledge base 
        2. POST  /ask      -> Chat API 

- Tech Stack 
    Language : Python 
    Backend Framework : Fast API 
    Database (if required ) : SQLite or PostgreSQL
    Vector Data Store : ChromaDB 
    LLM : Gemini, Gorq 
    LLM Tools Framework : Langchain  

- Project Folder Structure 
    ```bash
    
       Root_Repository 
        |    src
        |   |    main.py
        |   |    constant.py
        |   |    models.py
        |   |    ai_elements
        |   |    |     agent.py
        |   |    |     llm_tools.py
        |   |    |     llm.py
        |   |    |     prompts.py
        |   |    |     vector_store.py
        |   - .env.example
        |   - .gitignore
        |   - README.md
        
    ```
    I don't include route module initially. If more endpoint is required then Route module will be separated .
    


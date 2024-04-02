# Task 5 An Intelligent Chat Bot on the specialize domain Bus Booking Service.
 
- **Problem Statement** : A Conversational Chat API  to chat with end users regarding Bus Booking Information 
- **Client Requirements** : 
    An API Backend to chat with a Bot that provide as much as possible accurate information of Bus booking System and can also answers of the relevant questions of th Bus Booking System.




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
        |   |     main.py
        |   |     constant.py
        |   |     models.py
        |   |     ai_elements
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
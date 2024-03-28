#  Technical Documentation 
- **Problem Statement** : A Conversational Chat API  to chat with end users regarding Bus Booking Information 
- **Client Requirements** : 
    - An API Backend to chat with a Bot that provide as much as possible accurate information of Bus booking System and can also answers of the relevant questions of th Bus Booking System.
- **Solution Approach** : 
    - Step 1:
        - Collecting data about Bus terminus System in a document.(Creating  a Documen usnig  Chat GPT or Other resource for now)
        - Estimated Time : 5 hours
    - Step 2:
        - Index the document in Vector data store. 
        - Estimated Time : 2 hours
    - Step 3:
        - Creating a Chat System using the data of knowledge space of Vector Store. 
        - Estimated Time : 3 hours
    - Step 4:
        - Creating a Search Engine Tools that help to gather extra information that are not present in Knowledge sspace 
        - Estimated Time : 3 hours
    - Step 5:
        - Creating A General purpose LLM powered Agent to decide particular tools to handle the user requirements. 
        - Estimated Time : 4 hours
    - Step 6:
        - Creating A Fast API System to make access for all users. 
        - Estimated Time : 2 hours
    - Step 7: 
        - Bug Fixing and Documentation 
        - Estimated Time 2 Hours 
    
    - Total Estimated Time : 21 Hours: 
    - Total Estimate Day : 3 (excluding today)


    <br><br>

- Tech Stack 
    - Language : Python 
    - Backend Framework : Fast API 
    <!-- - Database (if required ) : SQLite or PostgreSQL -->
    - Vector Data Store : ChromaDB 
    - LLM : Gemini, Gorq 
    - LLM Tools Framework : Langchain  

- Project Folder Structure 
    ```bash
        Root_Repository 
        |---- WebApp
        |     |--- main.py
        |     |--- Required Module - 1
        |     |    | --- 
        |     |    | --- 
        |     |--- Required Module - 2
        |     |    | --- 
        |     |    | --- 
        | ---- .env.example
        | ---- .gitignore
        | ---- README.md
        
    ```
    I don't include route module initially. If more endpoint is required then Route module will be separated .
    



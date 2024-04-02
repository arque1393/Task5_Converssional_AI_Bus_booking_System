## For Annotation 
#%% 
from typing import Union,Sequence,Dict,Any
from langchain_core.documents import Document
from langchain_community.document_loaders import UnstructuredMarkdownLoader, TextLoader 
#%% 
# Import System Module 
from pathlib import Path 

# Import Custome Module 
# from src.elements.prompts import prompt_template #  Question Answer Prompt Template 
from src.constants import CACHE_DATASET,DATABASE_DIR,GOOGLE_API_KEY,LLM_MODEL_NAME


# Import Chroma db 
import chromadb 

# import langchain utilities 
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer \
import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAI 


# Import Google GenAI for Configuration 
import google.generativeai as genai
genai.configure(api_key=GOOGLE_API_KEY)



class MySentenceTransformerEmbeddings(SentenceTransformerEmbeddings):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def _embed_documents(self, texts):
        return super().embed_documents(texts)  
    def __call__(self, input):
        return self._embed_documents(input)    


# Checking Database Dir is exist or not 
if not DATABASE_DIR.is_dir():
    DATABASE_DIR.mkdir(parents=True)
if not CACHE_DATASET.is_dir():
    CACHE_DATASET.mkdir(parents=True)




# Creating Embedding Function
embedding_function = MySentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
# Creating LLM Tools 
llm = GoogleGenerativeAI(model=LLM_MODEL_NAME, google_api_key=GOOGLE_API_KEY)



class VectorStore(object):
    """Use Chroma Vector Store to store data """
    def __init__(self, username:str='DefaultUser', collection_name:str = 'DefaultCollection') -> None:
        self.username=username
        self.collection_name = collection_name
    def store_data(self,documents:Sequence[Document]) -> None:
         # Chroma DB Client Database Path
        persist_dir = DATABASE_DIR/self.username
    
        if not persist_dir.exists():
            persist_dir.mkdir(parents=True)
        client = chromadb.PersistentClient(str(persist_dir.resolve()))
        try:
            _  = client.create_collection(name=self.collection_name)
        except : 
            collection = client.get_collection(name=self.collection_name)
            # raise Exception(f"Collection {self.collection_name} is exist") 

        Chroma.from_documents(documents=documents,collection_name=self.collection_name,
                        embedding=embedding_function, 
                        persist_directory=persist_dir.resolve().as_posix())

    def similarity_search(self, query:str, k:int=5):
        client = chromadb.PersistentClient(str((DATABASE_DIR/self.username).resolve()))
        try:
            client.get_collection(self.collection_name)
        except:
            raise Exception(f"Collection {self.collection_name} not Found")

        chroma = Chroma(persist_directory=(DATABASE_DIR/self.username).resolve().as_posix(), 
                        embedding_function=embedding_function,
                        collection_name=self.collection_name)
        ## Retrive content form Document 
        docs = chroma.similarity_search(query,k)
        return docs
    
def upload_on_vector_db(file_path:Path,username:str|None = None, collection_name:str|None = None, ):
    """ 
    Upload content of a pdf file in Vector Database as knowledge space of an AI.
    Args:
        file_path (str): To locate exact file
        collection_name (str, optional): _description_. Defaults to "default".
    Raises:
        Exception: collection not found 
    Returns:
        Bool:True on success
    """
    # Loading PDF Document 
    if not file_path.exists():
        raise Exception("File Path not exist")
    file_extension = file_path.suffix
    if file_extension == '.pdf':
        loader = PyPDFLoader(str(file_path.resolve()))
    elif file_extension == '.md' : 
        loader = UnstructuredMarkdownLoader(str(file_path.resolve()))
    elif file_extension == '.txt':
        loader = TextLoader(str(file_path.resolve()))
    # Splitting documents in pages
    pages = loader.load_and_split()
    # Extract Text and divide into smaller documents Chunks
    documents_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=0)
    documents = documents_splitter.split_documents(pages)
    if username and collection_name:
        vc = VectorStore(username,collection_name)
    elif username:
        vc = VectorStore(username= username)
    elif collection_name:
        vc = VectorStore(collection_name=collection_name)
    else :
        vc = VectorStore() 
    vc.store_data(documents=documents)
    
    return True


# def get_answer(question:str, username:str='DefaultUser', collection_name:str = 'DefaultCollection', k  = 5):
#     """Make Query of the uploaded file 
#     This function retrieve data from Vector store and pass through a prompt of llm model and retrieve answer. 

#     Args:
#         question (str): Question String        
#         collection (str): collection name for select collection 
#     Return : 
#         str : Answer String 
#     """        
#     vc = VectorStore(username,collection_name)
#     docs = vc.similarity_search(query=question, k = k)
#     # print(docs)
 
#     ## Define Dara Retrival Chain from Prompt template and llm models 
#     chain = prompt_template | llm     
#     answer = chain.invoke(
#         {'knowledge':' '.join([page.page_content for page in docs]),
#         'question':question})
#     return answer

# # print(DATABASE_DIR)
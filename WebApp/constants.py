import os
from dotenv import load_dotenv
from pathlib import Path 
BASE_DIR = Path(__file__).resolve().parent
CACHE_DATASET = BASE_DIR/'cache_dir'
DATABASE_DIR = BASE_DIR/'ChromaDB'
TMP_FILE_PATH =BASE_DIR/'tmp_shg34gh4th8h97yert7gucm'
## Google API key 
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
# GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# # # Model Selection     
# LLM_MODEL_NAME = r'models/chat-bison-001'
# LLM_MODEL_NAME = r'models/text-bison-001'
LLM_MODEL_NAME = r'models/gemini-pro'
# LLM_MODEL_NAME = r'models//gemini-pro-version'
# LLM_MODEL_NAME = r'models/aqa'
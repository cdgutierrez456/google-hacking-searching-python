from dotenv import load_dotenv
import os

from googlesearch import GoogleSearch

# Cargamos las variables en el entorno
load_dotenv()

# Leemos la clave API
API_KEY_SERPAPI = os.getenv('API_KEY_SERPAPI')

query = 'filetype:sql "MySQL dump" (pass|password|passwd|pwd)'

gsearch = GoogleSearch(API_KEY_SERPAPI)

results = gsearch.search(query)

print(results)
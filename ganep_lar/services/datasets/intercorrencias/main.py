from insert_data import GetDataFromSheets, InsertData
from .models import IIntercorrencia as MODEL
from utils.unaccent import unaccent_and_lower

# Configurações
SHEETS_ID = "19xmv5ijBpgfQsukWsTx9B-otjf2X0gVHZ65fuKaunZ0"
SHEETS_TABLE_NAME = "Intercorrências"

def load_and_insert_data():
    # Obter dados do Google Sheets
    data = GetDataFromSheets(SHEETS_ID, SHEETS_TABLE_NAME, MODEL).get_data()

    # Inserir dados no banco de dados
    InsertData(data, (unaccent_and_lower(SHEETS_TABLE_NAME).replace(' ', '_'))).insert_data()







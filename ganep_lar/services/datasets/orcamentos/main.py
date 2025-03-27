# ATENDIMENTO	ID_ORCAMENTO	ID_COMPLEXIDADE	COMPLEXIDADE	DATA_INICIO	DATA_FINAL	DURACAO	RECEITA	CUSTO	RECEITA_MAT	RECEITA_EQP	RECEITA_UTI	RECEITA_MOD	RECEITA_PRC	RECEITA_EXM	RECEITA_DIA	CUSTO_MAT	CUSTO_EQP	CUSTO_UTI	CUSTO_MOD	CUSTO_PRC	CUSTO_EXM	CUSTO_DIA	CUSTO_TAX	OPERADORAfrom insert_data import GetDataFromSheets, insert_mongo_data
from insert_data import GetDataFromSheets, insert_mongo_data
from .models import IOrcamento as MODEL
from utils.unaccent import unaccent_and_lower
from pymongo import MongoClient

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Configurações
SHEETS_ID = "19xmv5ijBpgfQsukWsTx9B-otjf2X0gVHZ65fuKaunZ0"
SHEETS_TABLE_NAME = "Orçamentos"

def load_and_insert_data():
    # Obter dados do Google Sheets
    data = GetDataFromSheets(SHEETS_ID, SHEETS_TABLE_NAME, MODEL).get_data()

    # Inserir dados no banco de dados
    insert_mongo_data(unaccent_and_lower(SHEETS_TABLE_NAME).replace(' ', '_'), data)







import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from sqlalchemy import create_engine

# Configurações
SHEET_ID = "19xmv5ijBpgfQsukWsTx9B-otjf2X0gVHZ65fuKaunZ0"  # Substitua pelo ID do seu Google Sheet
DATABASE_URL = "postgresql://RPA:Ganep1175@localhost/GanepLar" 

class GetDataFromSheets:
    def __init__(self, sheet_id: str, sheet_name: str, class_model: object):
        self.sheet_id = sheet_id
        self.sheet_name = sheet_name
        self.credentials_file = "ganep_lar/services/google_sheets/credentials.json"
        self.class_model = class_model

    def get_data(self):
        # Autenticação
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, scope)
        client = gspread.authorize(creds)

        # Acessar a planilha
        sheet = client.open_by_key(self.sheet_id).worksheet(self.sheet_name)

        # Ler os dados
        data = sheet.get_all_records()

        # Converter para DataFrame
        df = pd.DataFrame(data)
        df_model = [self.class_model(**kwargs.to_dict()) for index, kwargs in df.iterrows()]
        df = pd.DataFrame([atendimento.__dict__() for atendimento in df_model])
        return df


# Inserir dados no banco de dados e criar a tabela automaticamente
class InsertData:
    def __init__(self, data: pd.DataFrame, table_name: str, method: str = "replace"):
        self.data = data
        self.engine = create_engine(DATABASE_URL)
        self.table_name = table_name
        self.method = method

    def insert_data(self):
        self.data.to_sql(
            self.table_name, 
            con=self.engine,       
            if_exists=self.method,  
            index=False       
        )
        print(self.data)
        print("Tabela criada e dados inseridos com sucesso!")
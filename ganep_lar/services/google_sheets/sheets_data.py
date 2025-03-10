import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("ganep-lar/dashboards/services/credentials.json", scope)
client = gspread.authorize(credentials)
spreadsheet = client.open_by_key("19xmv5ijBpgfQsukWsTx9B-otjf2X0gVHZ65fuKaunZ0")  
sheet = spreadsheet.worksheet("Atendimentos Completo") 
df = pd.DataFrame(sheet.get_all_records())
import pandas as pd
from cachetools import TTLCache, cached
from flask import jsonify, Request
from services.database import *

CACHE_MAPA_ATENDIMENTOS = TTLCache(maxsize=100, ttl=3600)

@cached(CACHE_MAPA_ATENDIMENTOS)
def get_atendimentos():
    with SessionLocal() as db:
        result = db.execute(text('SELECT * FROM mapa_atendimentos'))
        df = pd.DataFrame(result.mappings().all())

        # Tratar automaticamente colunas de data (NaT) e colunas numéricas (NaN)
        for col in df.columns:
            # Verificar se a coluna é do tipo datetime
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].apply(lambda x: x.isoformat() if pd.notna(x) else None)
            # Verificar se a coluna é numérica (int ou float)
            elif pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(0)  # Substituir NaN por 0 (ou outro valor padrão)

        return df

def get_data(request: Request):
    df_atendimentos = get_atendimentos()

    # Convert datetime columns to strings, replacing NaT with None
    

    # Convert the DataFrame to a list of dictionaries
    df_atendimentos_dict = df_atendimentos[:77].to_dict(orient='records')
    print(df_atendimentos_dict)

    return jsonify(df_atendimentos_dict), 200
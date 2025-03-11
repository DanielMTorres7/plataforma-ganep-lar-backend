import pandas as pd
from datetime import datetime
from cachetools import cached, TTLCache
from sqlalchemy import text
from services.database import SessionLocal
from typing import List, Optional
from flask import jsonify, Request


hoje = datetime.now()
inicio_ano = datetime(2024, 6, 1)

# Configuração do cache
cache_atendimentos = TTLCache(maxsize=100, ttl=3600)
@cached(cache_atendimentos)
def retrieve_data() -> pd.DataFrame:
    with SessionLocal() as db:
        result = db.execute(text('SELECT * FROM atendimentos_completo'))
        df = pd.DataFrame(result.mappings().all())
        return df
    
def get_values():
    atendimentos = retrieve_data()


    # Filtros
    atendimentos_filters = (
        (atendimentos['STATUS'] == 'Em atendimento') 
    )

    atendimentos = atendimentos[atendimentos_filters]

    n_atendimentos = atendimentos[atendimentos_filters].shape[0]
    n_risco_nutri = atendimentos[atendimentos['RISCO_NUTRI'] == True].shape[0]
    n_ID = atendimentos[atendimentos['GRUPO'] == 'ID'].shape[0]
    n_AD = atendimentos[atendimentos['GRUPO'] == 'AD'].shape[0]
    n_gtt = atendimentos[atendimentos['GTT'] == True].shape[0]
    n_sne = atendimentos[atendimentos['SNE'] == True].shape[0]
    n_diabetes = atendimentos[atendimentos['DIABETES'] == True].shape[0]

    return n_atendimentos, n_risco_nutri, n_ID, n_AD, n_gtt, n_sne, n_diabetes





def get_data(request: Request):
    """Endpoint para obter dados de LPPs e ScoreBraden."""
    data = request.json
    
    n_atendimentos, n_risco_nutri, n_ID, n_AD, n_gtt, n_sne, n_diabetes = get_values()

    # Resposta final
    data = {
        'n_atendimentos': n_atendimentos,
        'n_risco_nutri': n_risco_nutri,
        'n_ID': n_ID,
        'n_AD': n_AD,
        'n_gtt': n_gtt,
        'n_sne': n_sne,
        'n_diabetes': n_diabetes
    }
    return jsonify(data), 200
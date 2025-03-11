import pandas as pd
from datetime import datetime
from cachetools import cached, TTLCache
from sqlalchemy import text
from services.database import SessionLocal
from typing import List, Optional
from flask import jsonify, Request

# Configuração do cache


hoje = datetime.now()
inicio_ano = datetime(2024, 6, 1)
cache_a = TTLCache(maxsize=100, ttl=3600)
@cached(cache_a)
def get_atendimentos() -> pd.DataFrame:
    with SessionLocal() as db:
        result = db.execute(text('SELECT "ENTRADA", "STATUS", "ALTA", "MOTIVO_ALTA", "OPERADORA", "PACIENTE", "ATENDIMENTO", "PRONTUARIO" FROM atendimentos_completo'))
        df = pd.DataFrame(result.mappings().all())
        return df
    
cache_ccid = TTLCache(maxsize=100, ttl=3600)
@cached(cache_ccid)
def get_ccids() -> pd.DataFrame:
    with SessionLocal() as db:
        result = db.execute(text('SELECT "NOME_PACIENTE", "DATA_OCORRENCIA", "CNU_TIPO_INFECCAO", "OPERADORA", "TIPO_INFECCAO" FROM ccid'))
        df = pd.DataFrame(result.mappings().all())
        return df


def get_df(data_inicio: datetime, data_fim: datetime, operadoras: Optional[List[str]] = None) -> pd.DataFrame:
    """Obtém os dados de internações de forma eficiente."""
    # Obtém os atendimentos
    atendimentos = get_atendimentos()
    ccids = get_ccids()

    filtros_atendimentos = (
        (atendimentos['ENTRADA'].dt.normalize() <= data_fim) &
        (
            (
                (atendimentos['STATUS'] == 'Alta') &
                (atendimentos['ALTA'].dt.normalize() >= data_inicio)
            ) |
            (atendimentos['STATUS'] == 'Em atendimento')
        )
    )
    atendimentos = atendimentos[filtros_atendimentos]

    filtros_ccids = (
        (ccids['DATA_OCORRENCIA'] >= data_inicio) &
        (ccids['DATA_OCORRENCIA'] <= data_fim)
    )
    ccids = ccids[filtros_ccids]
    list_operadoras = [{'label': f'{op} : {ccids[ccids["OPERADORA"] == op].shape[0]}', 'value': op} for op in ccids['OPERADORA'].unique()]
    # Ordena as operadoras por quantidade de atendimentos (extraindo o número do label)
    list_operadoras = sorted(list_operadoras, key=lambda x: int(x['label'].split(' : ')[1]), reverse=True)

    if operadoras:
        atendimentos = atendimentos[atendimentos['OPERADORA'].isin(operadoras)]
        ccids = ccids[ccids['OPERADORA'].isin(operadoras)]

    n_ccids = len(ccids)
    n_itu = len(ccids[(ccids['CNU_TIPO_INFECCAO'] == 'ITU')])
    n_atendimentos = len(atendimentos)

    last_ccids = ccids.sort_values(by='DATA_OCORRENCIA', ascending=False).to_dict(orient='records')

    meses = pd.date_range(start=data_inicio, end=data_fim, freq='MS')
    df_infeccoes = []

    for mes in meses:
        fim_mes = mes.replace(day=1) + pd.DateOffset(months=1) - pd.DateOffset(days=1)
        
        mes_infeccoes = ccids[
            (ccids['DATA_OCORRENCIA'] >= mes) &
            (ccids['DATA_OCORRENCIA'] <= fim_mes)
        ]

        infeccoes = len(mes_infeccoes)
        itu = len(mes_infeccoes[mes_infeccoes['CNU_TIPO_INFECCAO'] == 'ITU'])

        atendimentos_mes = len(atendimentos[
            (atendimentos['ENTRADA'].dt.normalize() >= mes) &
            (atendimentos['ENTRADA'].dt.normalize() <= fim_mes)
        ])

        df_infeccoes.append({
            'mes': mes.strftime('%b/%Y'),
            'infeccoes': infeccoes,
            'itus': itu,
            'percentual': (itu / infeccoes) * 100 if infeccoes > 0 else 0,
            'atendimentos': atendimentos_mes,
            'meta': 7.5
        })

    return pd.DataFrame(df_infeccoes), n_atendimentos, n_ccids, n_itu, last_ccids, list_operadoras
    

def get_data(request: Request):
    """Endpoint para obter dados de LPPs e ScoreBraden."""
    data = request.json
    inicio = data.get("data_inicio")
    fim = data.get("data_fim")
    if not inicio or not fim:
        return jsonify({"error": "Os atributos 'data_inicio' e 'data_fim' são obrigatórios"}), 400
    
    operadoras = data.get("operadoras")
    data_inicio = pd.to_datetime(inicio, format='%Y-%m-%d', errors='coerce')
    data_fim = pd.to_datetime(fim, format='%Y-%m-%d', errors='coerce')


    df_internacoes, n_atendimentos, n_ccids, n_itu, tabela_ultimas_infeccoes, operadoras = get_df(data_inicio, data_fim, operadoras)
    # Resposta final
    data = {
        'atendimentos': n_atendimentos,
        'itus': n_itu,
        'infeccoes': n_ccids,
        'table_last_infeccoes': tabela_ultimas_infeccoes,
        'df_infeccoes': df_internacoes.to_dict(orient='records'),
        'operadoras': operadoras,  # Número total de LPPs no período
    }
    return jsonify(data), 200
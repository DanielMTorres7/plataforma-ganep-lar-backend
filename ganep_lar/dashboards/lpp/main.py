import pandas as pd
from datetime import datetime
from cachetools import cached, TTLCache
from sqlalchemy import text
from services.database import SessionLocal
from typing import List, Optional
from flask import jsonify, Request

# Configuração do cache
cache_a = TTLCache(maxsize=100, ttl=3600)
cache_i = TTLCache(maxsize=100, ttl=3600)

hoje = datetime.now()
inicio_ano = datetime(2024, 6, 1)

@cached(cache_a)
def get_atendimentos() -> pd.DataFrame:
    """Obtém os dados de atendimentos_completo e retorna um DataFrame."""
    with SessionLocal() as db:
        result = db.execute(text('SELECT "PRONTUARIO", "SCORE_BRADEN", "ENTRADA", "STATUS", "OPERADORA", "ALTA" FROM atendimentos_completo'))
        df = pd.DataFrame(result.mappings().all())
        return df

@cached(cache_i)
def get_intercorrencias() -> pd.DataFrame:
    """Obtém os dados de intercorrencias e retorna um DataFrame."""
    with SessionLocal() as db:
        result = db.execute(text('SELECT "CLASSIFICACAO", "DATA_INICIO", "PACIENTE", "OPERADORA", "ATENDIMENTO" FROM intercorrencias'))
        df = pd.DataFrame(result.mappings().all())
        return df

def get_df(data_inicio: datetime, data_fim: datetime, operadoras: Optional[List[str]] = None) -> tuple[pd.DataFrame, int, pd.DataFrame, int, List[dict]]:
    """Calcula o número de pacientes com ScoreBraden por mês."""
    atendimentos = get_atendimentos()
    intercorrencias = get_intercorrencias()

    # Filtra os atendimentos
    filtros_atendimentos = (
        (atendimentos['SCORE_BRADEN'].notna()) &
        (atendimentos['ENTRADA'] <= data_fim) &
        (
            ((atendimentos['STATUS'] == "Alta") & (atendimentos['ALTA'] >= data_inicio)) |
            (atendimentos['STATUS'] == "Em atendimento")
        )
    )

    # Filtra as intercorrências
    filtros_intercorrencias = (
        (intercorrencias['CLASSIFICACAO'] == "LPP") &
        (intercorrencias['DATA_INICIO'] >= data_inicio) &
        (intercorrencias['DATA_INICIO'] <= data_fim)
    )
    intercorrencias_filtradas = intercorrencias[filtros_intercorrencias]

    # Lista de operadoras
    # Ordena as operadoras por quantidade de atendimentos (extraindo o número do label)
    list_operadoras = [{'label': f'{op} : {intercorrencias_filtradas[intercorrencias_filtradas["OPERADORA"] == op].shape[0]}', 'value': op} for op in intercorrencias_filtradas['OPERADORA'].unique()]
    list_operadoras = sorted(list_operadoras, key=lambda x: int(x['label'].split(' : ')[1]), reverse=True)

    if operadoras:
        filtros_atendimentos &= atendimentos['OPERADORA'].isin(operadoras)
        intercorrencias_filtradas = intercorrencias_filtradas[intercorrencias_filtradas['OPERADORA'].isin(operadoras)]

    # Filtrar valores unicos de prontuario sem ser atendimentos.drop_duplicates(subset='PRONTUARIO')
    atendimentos = atendimentos.loc[~atendimentos['PRONTUARIO'].duplicated(keep='last')]
    atendimentos_filtrados = atendimentos[filtros_atendimentos]

    # Número total de LPPs e atendimentos
    n_lpps = len(intercorrencias_filtradas)
    n_atendimentos = len(atendimentos_filtrados)


    # Table de LPPs
    df_lpp = intercorrencias_filtradas[['PACIENTE', 'DATA_INICIO', 'OPERADORA', 'ATENDIMENTO']]
    lpp_table = df_lpp[:12].to_dict(orient='records')

    # Lista de meses no intervalo
    meses = pd.date_range(start=data_inicio, end=data_fim, freq='MS')
    
    # Contagem de ScoreBraden por mês
    score_braden_por_mes = [
        {
            'mes': mes.strftime('%b/%Y'), 
            'score_braden': count,
            'lpps': lpps,
            'percentual': round(lpps / count * 100, 2) if lpps > 0 else 0
        }
        for mes in meses
        for mes_inicio in [mes]
        for mes_fim in [mes + pd.DateOffset(months=1) - pd.DateOffset(days=1)]
        for count in [len(atendimentos_filtrados[
            (atendimentos_filtrados['ENTRADA'] <= mes_fim) &
            (
                ((atendimentos_filtrados['STATUS'] == "Alta") & (atendimentos_filtrados['ALTA'] >= mes_inicio)) |
                (atendimentos_filtrados['STATUS'] == "Em atendimento")
            )
        ])]
        for lpps in [
            len(intercorrencias_filtradas[
            (intercorrencias_filtradas['DATA_INICIO'] >= mes_inicio) &
            (intercorrencias_filtradas['DATA_INICIO'] <= mes_fim)
            ]
        ) if len(intercorrencias_filtradas) > 0 else 1]
    ]
    
    df = pd.DataFrame(score_braden_por_mes)
    return df, lpp_table, n_lpps, n_atendimentos, list_operadoras




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

    # Obtém os dados
    score_braden_mensal, lpp_table, n_lpps, score_braden_total, list_operadoras = get_df(data_inicio, data_fim, operadoras)
    
    # Resposta final
    data = {
        'lpp_table': lpp_table,
        'operadoras': list_operadoras,
        'score_braden_mensal': score_braden_mensal.to_dict(orient='records'),
        'pacientes_classificados_score_braden': score_braden_total,
        'numero_lpps': n_lpps,  # Número total de LPPs no período
    }
    return jsonify(data), 200
import pandas as pd
from datetime import datetime
from cachetools import cached, TTLCache
from sqlalchemy import text
from typing import List, Optional
from flask import jsonify, Request
from services.mongo import db

# Configuração do cache
cache_a = TTLCache(maxsize=100, ttl=3600)

hoje = datetime.now()
inicio_ano = datetime(2024, 6, 1)

@cached(cache_a)
def retrieve_data() -> pd.DataFrame:
    colecao_atendimentos = db["atendimentos_completo"]
    # Consulta todos os documentos na coleção
    dados = list(colecao_atendimentos.find())
    
    # Converte a lista de dicionários para um DataFrame
    df = pd.DataFrame(dados)
    df = df[["ENTRADA", "STATUS", "ALTA", "MOTIVO_ALTA", "OPERADORA", "PACIENTE", "ATENDIMENTO", "PRONTUARIO"]]
    
    return df


def get_df_internacoes(data_inicio: datetime, data_fim: datetime, operadoras: Optional[List[str]] = None) -> pd.DataFrame:
    """Obtém os dados de internações de forma eficiente."""
    # Obtém os atendimentos
    atendimentos = retrieve_data()

    pre_filter = (
        (atendimentos['ENTRADA'].dt.normalize() <= data_fim) &
        (
            (
                (atendimentos['STATUS'] == 'Alta') & 
                (atendimentos['ALTA'].dt.normalize() >= data_inicio)
            ) |
            (atendimentos['STATUS'] == 'Em atendimento')
        )
    )
    atendimentos = atendimentos[pre_filter]
    atendimentos = atendimentos.drop_duplicates(subset='ATENDIMENTO')
    list_operadoras = [{'label': f'{op} : {atendimentos[atendimentos["OPERADORA"] == op].shape[0]}', 'value': op} for op in atendimentos['OPERADORA'].unique()]
    # Ordena as operadoras por quantidade de atendimentos (extraindo o número do label)
    list_operadoras = sorted(list_operadoras, key=lambda x: int(x['label'].split(' : ')[1]), reverse=True)
    if operadoras:
        atendimentos = atendimentos[atendimentos['OPERADORA'].isin(operadoras)]
    altas = atendimentos[
        (atendimentos['STATUS'] == 'Alta') &
        (atendimentos['ALTA'].dt.normalize() >= data_inicio) &
        (atendimentos['ALTA'].dt.normalize() < data_fim) 
    ].copy()

    
    n_atendimentos = len(atendimentos)
    n_entradas = len(atendimentos[
        (atendimentos['ENTRADA'].dt.normalize() >= data_inicio) &
        (atendimentos['ENTRADA'].dt.normalize() < data_fim)
    ])
    n_altas = len(atendimentos[(
        (atendimentos['STATUS'] == 'Alta') & 
        (atendimentos['ALTA'].dt.normalize() >= data_inicio) &
        (atendimentos['ALTA'].dt.normalize() < data_fim)
    )])

    meses = pd.date_range(start=data_inicio, end=data_fim, freq='MS')
    df_atendimentos = [
        {
            'mes': mes.strftime('%b/%Y'),
            'entradas': len(atendimentos[
                (atendimentos['ENTRADA'].dt.normalize() >= mes) &
                (atendimentos['ENTRADA'].dt.normalize() < fim_mes)
            ]),
            'altas': len(atendimentos[
                (atendimentos['ALTA'].dt.normalize() >= mes) &
                (atendimentos['ALTA'].dt.normalize() < fim_mes)
            ]),
            'atendimentos': len(atendimentos[
                (atendimentos['ENTRADA'].dt.normalize() <= fim_mes) &
                (
                    (
                        (atendimentos['STATUS'] == 'Alta') & 
                        (atendimentos['ALTA'].dt.normalize() >= mes)
                    ) |
                    (atendimentos['STATUS'] == 'Em atendimento')
                )
            ]),
        }
        for mes in meses
        for fim_mes in [mes + pd.DateOffset(months=1) - pd.DateOffset(days=1)]
    ]
    # Lista de cada mes com a contagem de cada motivo de alta
    df_motivos = [
        {
            'mes': mes.strftime('%b/%Y'),
            'motivos': dict(sorted(altas[
                (altas['ALTA'].dt.normalize() >= mes) &
                (altas['ALTA'].dt.normalize() < fim_mes)
            ].groupby('MOTIVO_ALTA').size().to_dict().items(), key=lambda item: item[0]))
        }
        for mes in meses
        for fim_mes in [mes + pd.DateOffset(months=1) - pd.DateOffset(days=1)]
    ]


    # Criar um dict com os motivos de alta e os respectivos valores
    motivos = {}
    for alta in altas['MOTIVO_ALTA'].unique():
        if alta:
            motivos[alta] = altas[altas['MOTIVO_ALTA'] == alta].to_dict(orient='records')
    
    

    return pd.DataFrame(df_atendimentos), n_atendimentos, n_entradas, n_altas, list_operadoras, pd.DataFrame(df_motivos), motivos
   
   
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

    df_atendimentos, n_atendimentos, n_entradas, n_altas, list_operadoras, df_motivos, motivos = get_df_internacoes(data_inicio, data_fim, operadoras)
    # Resposta final
    data = {
        'atendimentos': n_atendimentos,
        'entradas': n_entradas,
        'altas': n_altas,
        'df_atendimentos': df_atendimentos.to_dict(orient='records'),
        'df_altas': df_motivos.to_dict(orient='records'),  # Adicione lógica para calcular, se necessário
        'operadoras': list_operadoras,  # Número total de LPPs no período
        'motivos': motivos
    }
    return jsonify(data), 200
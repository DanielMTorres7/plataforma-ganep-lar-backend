import pandas as pd
from datetime import datetime
from cachetools import cached, TTLCache
from flask import jsonify, Request
from typing import List, Optional
from pymongo import MongoClient
from services.mongo import db

cache_a = TTLCache(maxsize=100, ttl=3600)
@cached(cache_a)
def get_atendimentos() -> pd.DataFrame:
    """Obtém os dados de atendimentos_completo e retorna um DataFrame."""
    colecao_atendimentos = db["prontuarios"]
    # Consulta todos os documentos na coleção
    dados = list(colecao_atendimentos.find())
    
    # Converte a lista de dicionários para um DataFrame
    df = pd.DataFrame(dados)
    
    return df

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

    prontuarios = get_atendimentos()
    visitas = []
    intercorrencias = []
    ccids = []
    score_braden = []
    for prontuario in prontuarios.to_dict(orient='records'):
        for _, atendimento in prontuario['ATENDIMENTOS'].items():
            if atendimento['STATUS'] not in ['Alta', 'Em atendimento']:
                continue
            if atendimento['ENTRADA'] > data_fim or (atendimento['STATUS'] == 'Alta' and atendimento['ALTA'] < data_inicio):
                continue

            if atendimento['SCORE_BRADEN']:
                score_braden.append({
                    'PACIENTE': prontuario['PACIENTE'],
                    'PRONTUARIO': prontuario['PRONTUARIO'],
                    'ENTRADA': atendimento['ENTRADA'],
                    'STATUS': atendimento['STATUS'],
                    'ALTA': atendimento['ALTA'],
                    'OPERADORA': atendimento['OPERADORA']
                })

            for visita in atendimento['VISITAS']:
                # jan./25 -> 2025-01-25
                mes = datetime.strptime(visita['MES'], '%b./%y')
                if mes >= data_inicio and mes <= data_fim:
                    visitas.append({
                        'PACIENTE': prontuario['PACIENTE'],
                        'PRONTUARIO': prontuario['PRONTUARIO'],
                        'DATA': visita['MES'],
                        'OPERADORA': atendimento['OPERADORA']
                    })

            for ccid in atendimento['CCIDS']:
                if not ccid:
                    continue
                if ccid['DATA_OCORRENCIA'] >= data_inicio and ccid['DATA_OCORRENCIA'] <= data_fim:
                    ccids.append({
                        'PACIENTE': prontuario['PACIENTE'],
                        'PRONTUARIO': prontuario['PRONTUARIO'],
                        'DATA': ccid['DATA_OCORRENCIA'],
                        'TIPO_INFECCAO': ccid['TIPO_INFECCAO'],
                        'OPERADORA': atendimento['OPERADORA']
                    })

            for _, intercorrencia in atendimento['INTERCORRENCIAS'].items():
                if not intercorrencia:
                    continue
                if intercorrencia['DATA_INICIO'] >= data_inicio and intercorrencia['DATA_INICIO'] <= data_fim:
                    intercorrencias.append({
                        'PACIENTE': prontuario['PACIENTE'],
                        'PRONTUARIO': prontuario['PRONTUARIO'],
                        'DATA_INICIO': intercorrencia['DATA_INICIO'],
                        'OPERADORA': atendimento['OPERADORA']
                    })
    visitas = pd.DataFrame(visitas).groupby(['OPERADORA']).size().reset_index(name='VISITAS')
    ccids = pd.DataFrame(ccids).groupby(['OPERADORA']).size().reset_index(name='CCIDS')
    intercorrencias = pd.DataFrame(intercorrencias).groupby(['OPERADORA']).size().reset_index(name='INTERCORRENCIAS')
    score_braden = pd.DataFrame(score_braden).drop_duplicates(subset='PRONTUARIO', keep='last').groupby(['OPERADORA']).size().reset_index(name='SCORE_BRADEN')

    # unir os dataframes de visitas e intercorrencias
    df_operadoras = pd.merge(visitas, intercorrencias, on='OPERADORA', how='outer')
    df_operadoras = pd.merge(df_operadoras, ccids, on='OPERADORA', how='outer')
    df_operadoras = pd.merge(df_operadoras, score_braden, on='OPERADORA', how='outer')
    df_operadoras = df_operadoras.fillna(0)
    df_operadoras['INTERCORRENCIAS'] = df_operadoras['INTERCORRENCIAS'].astype(int)
    df_operadoras['CCIDS'] = df_operadoras['CCIDS'].astype(int)
    df_operadoras['VISITAS'] = df_operadoras['VISITAS'].astype(int)
    df_operadoras['SCORE_BRADEN'] = df_operadoras['SCORE_BRADEN'].astype(int)


    return jsonify(df_operadoras.to_dict(orient='records')), 200
            

    
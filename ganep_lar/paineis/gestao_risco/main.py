import pandas as pd
from datetime import datetime
from cachetools import cached, TTLCache
from sqlalchemy import text
from typing import List, Optional
from flask import jsonify, Request
from services.mongo import db

hoje = datetime.now()
inicio_ano = datetime(2024, 6, 1)

# Configuração do cache
cache_atendimentos = TTLCache(maxsize=100, ttl=3600)
@cached(cache_atendimentos)
def retrieve_data() -> pd.DataFrame:
    """Busca os dados do MongoDB e retorna um DataFrame."""
    colecao_atendimentos = db["prontuarios"]
    # Consulta todos os documentos na coleção
    dados = list(colecao_atendimentos.find())
    
    return dados
    
    
def get_values():
    prontuarios = retrieve_data()
    inicio_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    fim_mes = inicio_mes.replace(month=inicio_mes.month + 1)

    atendimentos = []
    visitas = []
    n_ccids = []

    
    for prontuario in prontuarios:
        for atendimento in prontuario['ATENDIMENTOS'].values():
            if atendimento['STATUS'] != 'Em atendimento':
                continue
            atendimentos.append({
                'ENTRADA': atendimento['ENTRADA'],
                'PACIENTE': prontuario['PACIENTE'],
                'OPERADORA': atendimento['OPERADORA'],
                'ATENDIMENTO': atendimento['ATENDIMENTO'],
                'PRONTUARIO': prontuario['PRONTUARIO'],
                'RISCO_NUTRI': atendimento['RISCO_NUTRI'],
                'GRUPO': atendimento['GRUPO'],
                'GTT': atendimento['GTT'],
                'SNE': atendimento['SNE'],
                'DIABETES': atendimento['DIABETES'],
                'TQT': atendimento['TQT'],
            })

            for ccid in atendimento['CCIDS']:
                if ccid['DATA_OCORRENCIA'] >= inicio_mes and ccid['DATA_OCORRENCIA'] < fim_mes:
                    n_ccids.append({
                        'ATENDIMENTO': atendimento['ATENDIMENTO'],
                        'TIPO_INFECCAO': ccid['TIPO_INFECCAO']
                    })

            for visita in atendimento['VISITAS']:
                # if visita['MES'] == datetime.now().strftime('%b./%y'):
                if visita['MES'] == 'fev./25':
                    visitas.append({
                        'ATENDIMENTO': atendimento['ATENDIMENTO'],
                        'ESPECIALIDADE': visita['ESPECIALIDADE'],
                        'VISITCOUNT': visita['VISITCOUNT'],
                        'PACIENTE': prontuario['PACIENTE'],
                        'OPERADORA': atendimento['OPERADORA'],
                        'PRONTUARIO': prontuario['PRONTUARIO'],
                    })

    # Unir os dados de atendimentos e ccids
    
    for ccid in n_ccids:
        for atendimento in atendimentos:
            if ccid['ATENDIMENTO'] == atendimento['ATENDIMENTO']:
                atendimento.update({'TIPO_INFECCAO': ccid['TIPO_INFECCAO']})
    atendimentos_df = pd.DataFrame(atendimentos)
    especialidades = []
    if visitas:
        visitas_df = pd.DataFrame(visitas)
        visitas_df['ESPECIALIDADE'] = visitas_df['ESPECIALIDADE'].str.upper().str.replace('  ', ' ').str.lstrip()
        visitas_df = visitas_df.groupby('ESPECIALIDADE')
        for especialidade, grupo in visitas_df:

            pacientes = grupo.groupby('PACIENTE')
            paciente_visitas = []
            for nome_paciente, grupo_paciente in pacientes:
                # Definir o ultimo paciente como paciente
                paciente = grupo_paciente.iloc[-1]
                paciente_visitas.append({
                    'PACIENTE': nome_paciente,
                    'VISITCOUNT': int(grupo_paciente['VISITCOUNT'].sum()),
                    'ATENDIMENTO': int(paciente['ATENDIMENTO']),
                    'OPERADORA': str(paciente['OPERADORA']),
                    'PRONTUARIO': int(paciente['PRONTUARIO']),
                })
            paciente_visitas = sorted(paciente_visitas, key=lambda x: x['VISITCOUNT'], reverse=True)
            especialidades.append({
                'VISITCOUNT': int(grupo['VISITCOUNT'].sum()),
                'PACIENTES': paciente_visitas,
                'ESPECIALIDADE': especialidade,
            })
        visitas_df = sorted(especialidades, key=lambda x: x['VISITCOUNT'], reverse=True)
    else:
        visitas_df = []

        
    n_atendimentos = len(atendimentos_df)
    n_risco_nutri = atendimentos_df[atendimentos_df['RISCO_NUTRI'] == True].replace({pd.NaT: None}).to_dict(orient='records')
    n_ID = atendimentos_df[atendimentos_df['GRUPO'] == 'ID'].replace({pd.NaT: None}).to_dict(orient='records')
    n_AD = atendimentos_df[atendimentos_df['GRUPO'] == 'AD'].replace({pd.NaT: None}).to_dict(orient='records')
    n_gtt = atendimentos_df[atendimentos_df['GTT'] == True].replace({pd.NaT: None}).to_dict(orient='records')
    n_sne = atendimentos_df[atendimentos_df['SNE'] == True].replace({pd.NaT: None}).to_dict(orient='records')
    n_tqt = atendimentos_df[atendimentos_df['TQT'] == True].replace({pd.NaT: None}).to_dict(orient='records')
    n_diabetes = atendimentos_df[atendimentos_df['DIABETES'] == True].replace({pd.NaT: None}).to_dict(orient='records')

    return n_atendimentos, n_risco_nutri, n_ID, n_AD, n_gtt, n_sne, n_diabetes, visitas_df, n_ccids, n_tqt





def get_data(request: Request):
    """Endpoint para obter dados de LPPs e ScoreBraden."""
    data = request.json
    
    n_atendimentos, n_risco_nutri, n_ID, n_AD, n_gtt, n_sne, n_diabetes, visitas_df, n_ccids, n_tqt = get_values()

    # Resposta final
    data = {
        'n_atendimentos': n_atendimentos,
        'n_risco_nutri': n_risco_nutri,
        'n_ID': n_ID,
        'n_AD': n_AD,
        'n_gtt': n_gtt,
        'n_sne': n_sne,
        'n_diabetes': n_diabetes,
        'visitas': visitas_df,
        'n_ccids': n_ccids,
        'n_tqt': n_tqt
    }
    return jsonify(data), 200
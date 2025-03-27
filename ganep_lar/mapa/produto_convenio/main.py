import pandas as pd
from datetime import datetime
from cachetools import TTLCache, cached
from typing import List
from services.mongo import db

from flask import jsonify, Request


CACHE_MAPA_ATENDIMENTOS = TTLCache(maxsize=100, ttl=3600)

@cached(CACHE_MAPA_ATENDIMENTOS)
def get_atendimentos():
    """Busca os dados do MongoDB e retorna um DataFrame."""
    colecao_atendimentos = db["mapa_atendimentos"]
    # Consulta todos os documentos na coleção
    dados = list(colecao_atendimentos.find())
    
    # Converte a lista de dicionários para um DataFrame
    df = pd.DataFrame(dados)
    
    return df

# def get_produtos_convenio(request: Request):
#     """Endpoint para obter dados de LPPs e ScoreBraden."""
#     data = request.json

#     data_inicio = pd.to_datetime(data.get("data_inicio"), format='%Y-%m-%d', errors='coerce') - pd.Timedelta(days=1)
#     data_fim = pd.to_datetime(data.get("data_fim"), format='%Y-%m-%d', errors='coerce')

#     prontuarios = get_atendimentos()
    
#     produtos = []
#     for prontuario in prontuarios:
#         for n_atendimento, atendimento in prontuario['ATENDIMENTOS'].items():
#             if atendimento['STATUS'] not in ['Alta', 'Em atendimento']:
#                 continue
#             if atendimento['OPERADORA'] == '' or atendimento['PROGRAMA'] == '':
#                 continue
#             if pd.isna(atendimento['ENTRADA']) or not atendimento['ENTRADA'] or atendimento['ENTRADA'] == "":
#                 continue
#             if atendimento['ENTRADA'] > data_fim or (atendimento['STATUS'] == 'Alta' and atendimento['ALTA'] < data_inicio):
#                 continue
#         operadora = atendimento['OPERADORA']
#         produto = atendimento['PROGRAMA'][5:]
#         entrada = atendimento['ENTRADA']
#         alta = atendimento['ALTA']
#         paciente = prontuario['PACIENTE']
#         status = atendimento['STATUS']
#         produtos.append({
#             "operadora": operadora,
#             "paciente": paciente,
#             "produto": produto,
#             "entrada": entrada,
#             "alta": alta,
#             'atendimento': n_atendimento,
#             'status': status
#         })

#     dias = pd.date_range(start=data_inicio, end=data_fim, freq='D')
#     produtos = pd.DataFrame(produtos)
#     final = []
#     produtos_operadora = produtos.groupby(['produto', 'operadora'])

#     for (produto, operadora), group in produtos_operadora:
#         diario = []
#         pacientes_ateriores = set()
#         for dia in dias:
#             pacientes_dia = set(group[
#                 (group['entrada'] <= dia) & 
#                 (group['alta'] >= dia)
#             ]['paciente'])
#             total_pacientes = len(pacientes_dia)
#             dados = {
#                 "dia": dia.strftime('%d/%m/%Y'),
#                 "total": total_pacientes
#             }
#             if len(diario) > 0:
#                 entradas = list(pacientes_dia - pacientes_ateriores)
#                 saidas = list(pacientes_ateriores - pacientes_dia)
#                 if len(entradas) > 0:
#                     dados["entradas"] = entradas
#                 if len(saidas) > 0:
#                     dados["saidas"] = saidas
#             pacientes_ateriores = pacientes_dia
#             diario.append(dados)

            
#         final.append({
#             "operadora": operadora,
#             "produto": produto,
#             "diario": diario,
#             "media": round(len(group) / len(dias), 1)
#         })
        
#     return {
#         "operadoras": final
#     }



def get_produtos_convenio(request: Request):
    """Endpoint para obter dados de LPPs e ScoreBraden."""
    data = request.json
    inicio = data.get("data_inicio")
    fim = data.get("data_fim")
    # Definir o início e o fim do mês
    mes_inicio = pd.to_datetime(inicio, format='%Y-%m-%d', errors='coerce')
    mes_fim = pd.to_datetime(fim, format='%Y-%m-%d', errors='coerce')

    df_atendimentos = get_atendimentos()

    # Filtrar os atendimentos que estão dentro do mês atual 
    filtro = (
    (
        df_atendimentos['ENTRADA'] <= mes_fim    
    ) & 
    (
        (pd.isna(df_atendimentos['ALTA'])) | 
        (df_atendimentos['ALTA'] >= mes_fim)
    ) & 
        (df_atendimentos['STATUS'] != "Reprovado")
    )
    df_filtrado = df_atendimentos[filtro]
    
    operadoras = []
    dias = pd.date_range(start=mes_inicio, end=mes_fim, freq='D')
    # Agrupar por operadora e obter os produtos únicos
    for (operadora, produto), group in df_filtrado.groupby(['OPERADORA', 'MODALIDADE']):
        diario = []
        total_pacientes = 0
        pacientes_anteriores = set()  # Usar um conjunto para facilitar a comparação
        # Para cada dia no intervalo
        for dia in dias:
            pacientes_dia = set([
                paciente['PACIENTE']
                for paciente in group.to_dict(orient='records')
                if (
                    paciente['ENTRADA'] <= dia and
                    (pd.isna(paciente['ALTA']) or paciente['ALTA'] >= dia)
                )
            ])
            total_pacientes += len(pacientes_dia)
            atts = {
                "dia": dia.strftime('%d/%m/%Y'),
                "total": len(pacientes_dia)
            }
            
            # Entradas e saídas com relação ao dia anterior, comparar a lista de pacientes
            if len(diario) > 0:
                entradas = list(pacientes_dia - pacientes_anteriores)
                saidas = list(pacientes_anteriores - pacientes_dia)
                if len(entradas) > 0:
                    atts["entradas"] = entradas
                if len(saidas) > 0:
                    atts["saidas"] = saidas
                    
            pacientes_anteriores = pacientes_dia
            diario.append(atts)

        # Calcular a média de pacientes por dia
        media = round(total_pacientes / len(dias), 1)

        # Adicionar ao resultado final
        operadoras.append({
            "operadora": operadora,
            "produto": produto,
            "diario": diario,
            "media": media
        })

    return {
        "operadoras": operadoras
    }
    
        
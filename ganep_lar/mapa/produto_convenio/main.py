import pandas as pd
from datetime import datetime
from cachetools import TTLCache, cached
from typing import List
from services.database import *

from flask import jsonify, Request


CACHE_MAPA_ATENDIMENTOS = TTLCache(maxsize=100, ttl=3600)

@cached(CACHE_MAPA_ATENDIMENTOS)
def get_atendimentos():
    with SessionLocal() as db:
        result = db.execute(text('SELECT "ENTRADA", "ALTA", "OPERADORA", "MODALIDADE", "STATUS", "PACIENTE" FROM mapa_atendimentos'))
        df = pd.DataFrame(result.mappings().all())
        return df

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
    filtro = (df_atendimentos['ENTRADA'] <= mes_fim) & ((df_atendimentos['ALTA'] >= mes_fim) | (df_atendimentos['ALTA'].isna()) & (df_atendimentos['STATUS'] != "Reprovado"))
    df_filtrado = df_atendimentos[filtro]
    
    operadoras = []
    dias = pd.date_range(start=mes_inicio, end=mes_fim, freq='D')
    # Agrupar por operadora e obter os produtos únicos
    for (operadora, produto), group in df_filtrado.groupby(['OPERADORA', 'MODALIDADE']):
        diario = []
        total_pacientes = 0
        pacientes_anteriores = []
        # Para cada dia no intervalo
        for dia in dias:
            pacientes_dia = set([
                paciente['PACIENTE']
                for paciente in group.to_dict(orient='records')
                if (
                    paciente['ENTRADA'] <= dia and
                    (pd.isna(paciente['ALTA']) or paciente['ALTA'] > dia)
                )
            ])
            total_pacientes += len(pacientes_dia)
            atts = {
                "dia": dia.strftime('%d/%m/%Y'),
                "total": len(pacientes_dia)
            }
            
            # Entradas e saidas com relação ao dia anterior, comparar a lista de pacientes
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
    
        
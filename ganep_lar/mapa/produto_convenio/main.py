import pandas as pd
from datetime import datetime
from cachetools import TTLCache, cached
from typing import List
from services.database import *


CACHE_MAPA_ATENDIMENTOS = TTLCache(maxsize=100, ttl=3600)

@cached(CACHE_MAPA_ATENDIMENTOS)
def get_atendimentos():
    with SessionLocal() as db:
        result = db.execute(text('SELECT "ENTRADA", "ALTA", "OPERADORA", "MODALIDADE", "STATUS", "PACIENTE" FROM mapa_atendimentos'))
        df = pd.DataFrame(result.mappings().all())
        return df

def get_produtos_convenio():
    # Definir o início e o fim do mês
    mes_inicio = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    mes_fim = datetime.now()

    df_atendimentos = get_atendimentos()

    # Filtrar os atendimentos que estão dentro do mês atual 
    filtro = (df_atendimentos['ENTRADA'] <= mes_fim) & ((df_atendimentos['ALTA'] >= mes_fim) | (df_atendimentos['ALTA'].isna()))
    df_filtrado = df_atendimentos[filtro]
    
    operadoras = []
    dias = pd.date_range(start=mes_inicio, end=mes_fim, freq='D')
    # Agrupar por operadora e obter os produtos únicos
    for (operadora, produto), group in df_filtrado.groupby(['OPERADORA', 'MODALIDADE']):
        diario = []
        total_pacientes = 0

        # Preprocessamento: filtrar pacientes válidos para o produto
        pacientes_validos = [
            paciente for _, paciente in group.iterrows()
            if paciente['STATUS'] != "Reprovado"
        ]
        pacientes_anteriores = []
        # Para cada dia no intervalo
        for dia in dias:
            pacientes_dia = set([
                paciente['PACIENTE']
                for paciente in pacientes_validos
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
    
        
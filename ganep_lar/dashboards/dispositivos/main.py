import pandas as pd
from datetime import datetime
from cachetools import cached, TTLCache
from sqlalchemy import text
from services.database import SessionLocal
from typing import List, Optional
from flask import jsonify, Request

# Configuração do cache
cache_a = TTLCache(maxsize=100, ttl=3600)

hoje = datetime.now()
inicio_ano = datetime(2024, 6, 1)

# TQT
# GTT
# SNE
# CVD
# CVA
# PICC


@cached(cache_a)
def retrieve_data() -> pd.DataFrame:
    with SessionLocal() as db:
        result = db.execute(text('SELECT "PRONTUARIO", "PACIENTE", "ENTRADA", "STATUS", "TQT", "GTT", "SNE", "CVD", "CVA", "PICC", "OPERADORA", "ATENDIMENTO", "ALTA" FROM atendimentos_completo'))
        df = pd.DataFrame(result.mappings().all())
        

        return df


def get_df_dispositivos(data_inicio: datetime, data_fim: datetime, operadoras: Optional[List[str]] = None) -> pd.DataFrame:
    """Obtém os dados de internações de forma eficiente."""
    # Obtém os atendimentos
    atendimentos = retrieve_data()

    filters = (
        (atendimentos['ENTRADA'].dt.normalize() <= data_fim) &
        (
            ((atendimentos['STATUS'] == 'Alta') & (atendimentos['ALTA'].dt.normalize() >= data_inicio)) |
            (atendimentos['STATUS'] == 'Em atendimento')
        ) &
        (
            atendimentos['TQT'] | 
            atendimentos['GTT'] |
            atendimentos['SNE'] |
            atendimentos['CVD'] |
            atendimentos['CVA'] |
            atendimentos['PICC']
        )
    )

    # filtrar valores unicos de ATENDIMENTO
    atendimentos = atendimentos[filters].drop_duplicates(subset='ATENDIMENTO')
    list_operadoras = [{'label': f'{op} : {atendimentos[atendimentos["OPERADORA"] == op].shape[0]}', 'value': op} for op in atendimentos['OPERADORA'].unique()]
    # Ordena as operadoras por quantidade de atendimentos (extraindo o número do label)
    list_operadoras = sorted(list_operadoras, key=lambda x: int(x['label'].split(' : ')[1]), reverse=True)

    if operadoras:
        atendimentos = atendimentos[atendimentos['OPERADORA'].isin(operadoras)]

    n_atendimentos = len(atendimentos)

    n_tqt = atendimentos[(atendimentos['TQT'])].replace({pd.NaT: None}).to_dict(orient='records')
    n_gtt = atendimentos[(atendimentos['GTT'])].replace({pd.NaT: None}).to_dict(orient='records')
    n_sne = atendimentos[(atendimentos['SNE'])].replace({pd.NaT: None}).to_dict(orient='records')
    n_cvd = atendimentos[(atendimentos['CVD'])].replace({pd.NaT: None}).to_dict(orient='records')
    n_cva = atendimentos[(atendimentos['CVA'])].replace({pd.NaT: None}).to_dict(orient='records')
    n_picc = atendimentos[(atendimentos['PICC'])].replace({pd.NaT: None}).to_dict(orient='records')


    # Gera o intervalo de meses
    meses = pd.date_range(start=data_inicio, end=data_fim, freq='MS')

    # Lista para armazenar os dados mensais
    dados_mensais = []

    for mes in meses:
        inicio_mes = mes.replace(day=1)
        fim_mes = (mes + pd.DateOffset(months=1) - pd.DateOffset(days=1))

        atendimentos_mes = atendimentos[
            (atendimentos['ENTRADA'].dt.normalize() <= fim_mes) &
            (
                ((atendimentos['STATUS'] == 'Alta') & (atendimentos['ALTA'].dt.normalize() >= inicio_mes)) |
                (atendimentos['STATUS'] == 'Em atendimento')
            )
        ].copy()

        tqt = len(atendimentos_mes[(atendimentos_mes['TQT'])])
        
        gtt = len(atendimentos_mes[(atendimentos_mes['GTT'])])

        sne = len(atendimentos_mes[(atendimentos_mes['SNE'])])
        
        cvd = len(atendimentos_mes[(atendimentos_mes['CVD'])])

        cva = len(atendimentos_mes[(atendimentos_mes['CVA'])])

        picc = len(atendimentos_mes[(atendimentos_mes['PICC'])])

        # Adiciona os dados do mês à lista
        dados_mensais.append({
            'mes': mes.strftime('%b/%Y'),
            'tqt': tqt,
            'gtt': gtt,
            'sne': sne,
            'cvd': cvd,
            'cva': cva,
            'picc': picc,
        })

    # Cria o DataFrame
    df_dispositivos = pd.DataFrame(dados_mensais)

    return df_dispositivos, n_tqt, n_gtt, n_sne, n_cvd, n_cva, n_picc, n_atendimentos, list_operadoras
    

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

    df_dispositivos, n_tqt, n_gtt, n_sne, n_cvd, n_cva, n_picc, n_atendimentos, list_operadoras = get_df_dispositivos(data_inicio, data_fim, operadoras)
    # Resposta final
    data = {
        'atendimentos': n_atendimentos,
        'tqt': n_tqt,
        'gtt': n_gtt,
        'sne': n_sne,
        'cvd': n_cvd,
        'cva': n_cva,
        'picc': n_picc,  # Adicione lógica para calcular, se necessário
        'df_dispositivos': df_dispositivos.to_dict(orient='records'),  # Número total de LPPs no período
        'operadoras': list_operadoras,  # Número total de LPPs no período
    }
    return jsonify(data), 200
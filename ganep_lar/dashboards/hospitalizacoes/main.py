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

@cached(cache_a)
def retrieve_data() -> pd.DataFrame:
    with SessionLocal() as db:
        result = db.execute(text('SELECT "ENTRADA", "STATUS", "ALTA", "MOTIVO_ALTA", "OPERADORA", "PACIENTE", "ATENDIMENTO", "PRONTUARIO" FROM atendimentos_completo'))
        df = pd.DataFrame(result.mappings().all())
        return df


def get_last_hosp_table_events(data_inicio: datetime, data_fim: datetime, operadoras) -> pd.DataFrame:
    """Obtém os últimos eventos de hospitalização."""
    atendimentos = retrieve_data()

    filtros = (
        (atendimentos['ENTRADA'] <= data_fim) &
        (atendimentos['STATUS'] == 'Alta') &
        atendimentos['ALTA'].notnull() &
        (atendimentos['ALTA'] >= data_inicio) &
        (atendimentos['MOTIVO_ALTA'] == 'Hospitalização')
    )
    if operadoras:
        filtros &= (atendimentos['OPERADORA'].isin(operadoras))
    
    atendimentos = atendimentos[filtros]

    df = pd.DataFrame([
        {
            'data': atend['ALTA'],
            'paciente': atend['PACIENTE'],
            'operadora': atend['OPERADORA']
        }
        for _, atend in atendimentos.iterrows()
    ][:12]).sort_values(by='data', ascending=False)
    return df

import pandas as pd
from datetime import datetime
from typing import List, Optional

def get_df_internacoes(data_inicio: datetime, data_fim: datetime, operadoras: Optional[List[str]] = None) -> pd.DataFrame:
    """Obtém os dados de internações de forma eficiente."""
    # Obtém os atendimentos
    atendimentos = retrieve_data()

    n_atendimentos = len(atendimentos[
        (atendimentos['ENTRADA'].dt.normalize() <= data_fim) &
        (
            ((atendimentos['STATUS'] == 'Alta') & (atendimentos['ALTA'].dt.normalize() >= data_inicio)) |
            (atendimentos['STATUS'] == 'Em atendimento')
        )
    ])

    # Filtra as internações
    filtros_internacoes = (
        (atendimentos['ENTRADA'].dt.normalize() <= data_fim) &
        (atendimentos['STATUS'] == 'Alta') &
        (atendimentos['ALTA'].dt.normalize() >= data_inicio) &
        (atendimentos['MOTIVO_ALTA'] == 'Hospitalização')
    )
    internacoes = atendimentos[filtros_internacoes].copy()

    # Lista de operadoras
    list_operadoras = [{'label': f'{op} : {internacoes[internacoes["OPERADORA"] == op].shape[0]}', 'value': op} for op in internacoes['OPERADORA'].unique()]
    # Ordena as operadoras por quantidade de atendimentos (extraindo o número do label)
    list_operadoras = sorted(list_operadoras, key=lambda x: int(x['label'].split(' : ')[1]), reverse=True)
    # Filtra por operadoras, se fornecido
    if operadoras:
        internacoes = internacoes[internacoes['OPERADORA'].isin(operadoras)]

    # Gera o intervalo de meses
    meses = pd.date_range(start=data_inicio, end=data_fim, freq='MS')

    n_internacoes = len(internacoes)

    # Lista para armazenar os dados mensais
    dados_mensais = []

    for mes in meses:
        inicio_mes = mes.replace(day=1)
        fim_mes = (mes + pd.DateOffset(months=1) - pd.DateOffset(days=1))

        # Filtra internações no mês
        filtro_mes_internacoes = (
            (internacoes['ENTRADA'].dt.normalize() <= fim_mes) &
            (internacoes['ALTA'].dt.normalize() >= inicio_mes) &
            (internacoes['ALTA'].dt.normalize() <= fim_mes)
        )
        internacoes_mes = internacoes[filtro_mes_internacoes].drop_duplicates(subset='ATENDIMENTO', keep='last')
        num_internacoes = len(internacoes_mes)

        # Filtra atendimentos no mês
        filtro_mes_atendimentos = (
            (atendimentos['ENTRADA'].dt.normalize() <= fim_mes) &
            (
                ((atendimentos['STATUS'] == 'Alta') & (atendimentos['ALTA'].dt.normalize() >= inicio_mes)) |
                (atendimentos['STATUS'] == 'Em atendimento')
            )
        )
        atendimentos_mes = atendimentos[filtro_mes_atendimentos].drop_duplicates(subset='PRONTUARIO', keep='last')
        num_atendimentos = len(atendimentos_mes)

        # Calcula a porcentagem
        porcentagem = round(num_internacoes / num_atendimentos, 3)*100 if num_atendimentos > 0 else 0

        # Adiciona os dados do mês à lista
        dados_mensais.append({
            'mes': mes.strftime('%b/%Y'),
            'internacoes': num_internacoes,
            'atendimentos': num_atendimentos,
            'meta': 9,  # Meta fixa
            'percentual': porcentagem
        })

    # Cria o DataFrame
    df_internacoes = pd.DataFrame(dados_mensais)


    return df_internacoes, list_operadoras, n_atendimentos, n_internacoes
    

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

    tabela_ultimas_hospitalizacoes = get_last_hosp_table_events(data_inicio, data_fim, operadoras).to_dict(orient='records')
    df_internacoes, operadoras, atendimentos, internacoes = get_df_internacoes(data_inicio, data_fim, operadoras)
    # Resposta final
    data = {
        'atendimentos': atendimentos,
        'internacoes': internacoes,
        'altas': 0,
        'df_internacoes': df_internacoes.to_dict(orient='records'),
        'table_ultimas_hospitalizacoes': tabela_ultimas_hospitalizacoes,  # Adicione lógica para calcular, se necessário
        'operadoras': operadoras,  # Número total de LPPs no período
    }
    return jsonify(data), 200
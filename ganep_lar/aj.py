from datetime import datetime
from typing import List, Optional
from services.mongo import db
import pandas as pd

def get_atendimentos() -> pd.DataFrame:
    """Busca os dados do MongoDB e retorna um DataFrame."""
    colecao_atendimentos = db["prontuarios"]
    # Consulta todos os documentos na coleção
    dados = list(colecao_atendimentos.find())
    
    # Converte a lista de dicionários para um DataFrame
    df = pd.DataFrame(dados)
    
    return df

def get_df(data_inicio: datetime, data_fim: datetime, operadoras: Optional[List[str]] = None) -> tuple[pd.DataFrame, int, pd.DataFrame, int, List[dict]]:
    """Calcula o número de pacientes com ScoreBraden por mês."""
    prontuarios = get_atendimentos()

    lpps = []
    scorebradens = []
    for prontuario in prontuarios.to_dict(orient='records'):
        atendimentos = prontuario['ATENDIMENTOS']
        # get atendimentos keys
        for a_key in atendimentos:
            atendimento = atendimentos[a_key]
            if atendimento['STATUS'] not in ['Alta', 'Em atendimento']:
                continue
            if atendimento['ENTRADA'] >= data_fim or (atendimento['STATUS'] == 'Alta' and atendimento['ALTA'] <= data_inicio):
                continue

            if atendimento['SCORE_BRADEN']:
                scorebradens.append({
                    'PACIENTE': prontuario['PACIENTE'],
                    'PRONTUARIO': prontuario['PRONTUARIO'],
                    'ENTRADA': atendimento['ENTRADA'],
                    'STATUS': atendimento['STATUS'],
                    'ALTA': atendimento['ALTA'],
                    'OPERADORA': atendimento['OPERADORA']
                })
            intercorrencias = atendimento['INTERCORRENCIAS']
            for inter_key in intercorrencias:
                inter = intercorrencias[inter_key]
                if not inter:
                    continue
                if inter['CLASSIFICACAO'] == 'LPP' and inter['DATA_INICIO'] >= data_inicio and inter['DATA_INICIO'] <= data_fim:
                    lpps.append({
                        'PACIENTE': prontuario['PACIENTE'],
                        'PRONTUARIO': prontuario['PRONTUARIO'],
                        'DATA_INICIO': inter['DATA_INICIO'],
                        'OPERADORA': atendimento['OPERADORA']
                    })
    lpp_table = pd.DataFrame(lpps).sort_values(by='DATA_INICIO')
    scorebradens = pd.DataFrame(scorebradens).drop_duplicates(subset='PRONTUARIO')
    if operadoras:
        scorebradens = scorebradens[scorebradens['OPERADORA'].isin(operadoras)]
        lpp_table = lpp_table[lpp_table['OPERADORA'].isin(operadoras)]
    
    df = lpp_table.groupby(lpp_table['DATA_INICIO'].dt.to_period('M')).size()
    n_lpps = lpp_table.shape[0]  # Número total de LPPs no período

    n_atendimentos = prontuarios.shape[0]
    list_operadoras = lpp_table['OPERADORA'].unique().tolist()

    # Contar mensalmente os pacientes com ScoreBraden no período de interesse
    score_mensal = []
    for mes in pd.date_range(start=data_inicio, end=data_fim, freq='M'):
        scorebradens_mes = len(scorebradens[
            (scorebradens['ENTRADA'] <= mes + pd.DateOffset(months=1)) &
            ((scorebradens['STATUS'] == 'Alta') & (scorebradens['ALTA'] >= mes) | 
            (scorebradens['STATUS'] == 'Em atendimento'))
        ])

        lpps_mes = lpp_table[lpp_table['DATA_INICIO'].dt.to_period('M') == mes.to_period('M')].shape[0]
        percentual = round(lpps_mes / scorebradens_mes * 100, 2) if lpps_mes > 0 else 0
        score_mensal.append(
            {
                'mes': mes,
                'score_braden': scorebradens_mes,
                'lpps': lpps_mes,
                'percentual': percentual
            }
        )

    score_mensal = pd.DataFrame(score_mensal).sort_values(by='mes')



    return score_mensal, lpp_table, n_lpps, n_atendimentos, list_operadoras


inicio_ano = datetime(2024, 1, 1)
hoje = datetime(2024, 12, 31)

inicio = datetime.now()
res = get_df(inicio_ano, hoje)
print(res)
print(f"demorou {datetime.now() - inicio}")

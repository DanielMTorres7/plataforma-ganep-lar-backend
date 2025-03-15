from services.mongo import db
import pandas as pd
from flask import jsonify, Request

def get_atend(pront:int):
    def get_atendimentos():
        """Busca os dados do MongoDB e retorna um DataFrame."""
        colecao_atendimentos = db["atendimentos_completo"]
        # Consulta todos os documentos na coleção
        dados = list(colecao_atendimentos.find())
        
        # Converte a lista de dicionários para um DataFrame
        df = pd.DataFrame(dados)
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].astype(object).where(df[col].notnull(), None)
            # NaN
            if pd.api.types.is_float_dtype(df[col]):
                df[col] = df[col].astype(object).where(df[col].notnull(), None)

        return df

    def get_intercorrencias():
        """Obtém os dados de intercorrencias e retorna um DataFrame."""
        # SELECT "CLASSIFICACAO", "DATA_INICIO", "PACIENTE", "OPERADORA", "ATENDIMENTO" FROM intercorrencias
        colecao_intercorrencias = db["intercorrencias"]
        dados = list(colecao_intercorrencias.find())

        df = pd.DataFrame(dados)
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].astype(object).where(df[col].notnull(), None)
            if pd.api.types.is_float_dtype(df[col]):
                df[col] = df[col].astype(object).where(df[col].notnull(), None)
        return df


    atendimentos = get_atendimentos()
    # atendimentos = atendimentos[(atendimentos["PRONTUARIO"] == pront)]
    intercorrencias = get_intercorrencias()

    # Filtra os atendimentos une os atendimentos por prontuário
    a = [
        {
            "PACIENTE" : paciente,
            "PRONTUARIO" : prointuario,
            "NASCIMENTO" : nascimento,
            "SEXO" : sexo,
            "ATENDIMENTOS" : atends
        }
        for _, p_atendimentos in atendimentos.drop_duplicates(subset="PRONTUARIO").iterrows()
        for paciente, prointuario, nascimento, sexo, atends in [
            (   
                p_atendimentos["PACIENTE"],
                p_atendimentos["PRONTUARIO"],
                p_atendimentos["NASCIMENTO"],
                p_atendimentos["SEXO"],
                {
                    str(atend["ATENDIMENTO"]): {
                        **atend.drop(["PACIENTE", "PRONTUARIO", "NASCIMENTO", "SEXO", "_id"]).to_dict(),
                        "INTERCORRENCIAS": {
                            str(intercorrencia['ID']): {**intercorrencia.drop(["PACIENTE", "OPERADORA", "ATENDIMENTO", "_id", "ID"]).to_dict()}
                            for _, intercorrencia in intercorrencias[intercorrencias["ATENDIMENTO"] == atend["ATENDIMENTO"]].iterrows()
                        }
                    }
                    for _, atend in atendimentos[atendimentos["PRONTUARIO"] == p_atendimentos["PRONTUARIO"]].iterrows()
                }
            )
        ]
    ]
    return a

at = get_atend(1)
# Inserir dados no banco de dados e criar a tabela automaticamente
colecao = db["prontuarios"]
colecao.insert_many(at)
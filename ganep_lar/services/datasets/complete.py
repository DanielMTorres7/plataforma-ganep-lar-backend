from datetime import datetime
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["GanepLar"]
import pandas as pd


def get_atend(pront:int):
    def get_data(dataset:str):
        """Busca os dados do MongoDB e retorna um DataFrame."""
        colecao_atendimentos = db[dataset]
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


    atendimentos = get_data("atendimentos_completo")
    intercorrencias = get_data("intercorrencias")
    ccids = get_data("ccids")
    visitas = get_data("visitas")
    orcamentos = get_data("orcamentos")
    equipe = get_data("equipe")

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
                        },
                        "CCIDS": [
                            {**ccid.drop(["NOME_PACIENTE", "INICIO_ATENDIMENTO", "OPERADORA", "ATENDIMENTO", "SEXO", "_id"]).to_dict()}
                            for _, ccid in ccids[ccids["ATENDIMENTO"] == atend["ATENDIMENTO"]].iterrows()
                        ],
                        "VISITAS": [
                            {**visita.drop(["PACIENTE", "NR_ATENDIMENTO", "_id"]).to_dict()}
                            for _, visita in visitas[visitas["NR_ATENDIMENTO"] == atend["ATENDIMENTO"]].iterrows()
                        ],
                        "ORCAMENTOS": {
                            str(orcamento["ID_ORCAMENTO"]): {**orcamento.drop(["ATENDIMENTO", "_id", "ID_ORCAMENTO", "OPERADORA"]).to_dict()}
                            for _, orcamento in orcamentos[orcamentos["ATENDIMENTO"] == atend["ATENDIMENTO"]].iterrows()
                        },
                        "EQUIPE": [
                            {**membro.drop(["ATENDIMENTO", "_id", "PATIENTNAME"]).to_dict()}
                            for _, membro in equipe[equipe["ATENDIMENTO"] == atend["ATENDIMENTO"]].iterrows()
                        ]
                    }
                    for _, atend in atendimentos[atendimentos["PRONTUARIO"] == p_atendimentos["PRONTUARIO"]].iterrows()
                }
            )
        ]
    ]
    return a

at = get_atend(1)
# Inserir dados no banco de dados e criar a tabela automaticamente

# print(at)
colecao = db["prontuarios"]
colecao.insert_many(at)
import pandas as pd

from .models.model_mapa_atendimento import ModelMapaAtendimento as MODEL
from insert_data import insert_mongo_data


def load_and_insert_data():
    data = pd.read_csv('ganep_lar/services/datasets/mapa_atendimentos/data/Mapa_Atendimentos.csv', encoding='Utf-8')

    # Converter para DataFrame
    df = pd.DataFrame(data)
    # Converter os tipos de dados
    atendimentos = [MODEL(**kwargs.to_dict()) for index, kwargs in df.iterrows()]
    df_filtrado = pd.DataFrame([atendimento.__dict__() for atendimento in atendimentos])

    insert_mongo_data('mapa_atendimentos', df_filtrado)
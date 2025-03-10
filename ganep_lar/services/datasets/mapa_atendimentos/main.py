import pandas as pd

from .models.model_mapa_atendimento import ModelMapaAtendimento as MODEL
from insert_data import InsertData


def load_and_insert_data():
    data = pd.read_csv('ganep_lar/services/datasets/mapa_atendimentos/data/Mapa_Atendimentos.csv', encoding='Utf-8')

    # Converter para DataFrame
    df = pd.DataFrame(data)

    # Converter os tipos de dados
    atendimentos = [MODEL(**kwargs.to_dict()) for index, kwargs in df.iterrows()]
    df_filtrado = pd.DataFrame([atendimento.__dict__() for atendimento in atendimentos])

    InsertData(df_filtrado, 'mapa_atendimentos').insert_data()
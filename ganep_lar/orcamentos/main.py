import pandas as pd
from orcamentos.models import *
from cachetools import cached, TTLCache
from flask import jsonify, Request
lista_campos_numericos = [
    "VLCSTDIA",
    "VLORCDIA",
    "VLCSTMOD",
    "VLORCMOD",
    "VLCSTMAT",
    "VLORCMAT",
    "VLCSTEQG",
    "VLORCEQG",
    "VLCSTOUT",
    "VLORCOUT",
    "CUSTONAOORCADO",
    "VLORCADO",
    "VLCUSTO",
    "RECEITANAOREALIZADA",
    "VLCSTIMP",
    "VLTOTCSTMOD",
    "VLTOTCSTMAT",
    "VLTOTCSTEQG",
    "VLTOTCSTOUT",
]

cache_i = TTLCache(maxsize=100, ttl=3600)
@cached(cache_i)
def get_orcamentos():
    file = 'ganep_lar/orcamentos/data/AMIGO.csv'
    df = pd.read_csv(file, encoding='Utf-8')
    retorno = []
    regionais = df['REGIONAL'].unique()
    for campo in set(lista_campos_numericos):
        try:
            df[campo] = df[campo].str.replace('.', '').str.replace(',', '.')
            df[campo] = df[campo].astype(float)
        except:
            pass
    geral = DfInfos(df, "Geral")
    for regiao in regionais:
        convenios = df[df['REGIONAL'] == regiao]['ENTERPRISENAME'].unique()
        df_regiao = df[df['REGIONAL'] == regiao].copy()
        regional = DfInfos(df_regiao, regiao)
        for convenio in convenios:
            df_convenio = df_regiao[df_regiao['ENTERPRISENAME'] == convenio].copy()
            # Gerar planilha de atendimentos por convenio
            df_pacientes = [Atendimento(**kwargs) for index, kwargs in df_convenio.iterrows()]

            planilhaAtendimentos = [PlanilhaAtendimentos(atendimento).__dict__() for atendimento in df_pacientes]
            convenial = DfInfos(df_convenio, convenio)
            convenial.add_child(planilhaAtendimentos)
            regional.add_child(convenial.get_info())
        geral.add_child(regional.get_info())
    retorno = geral.get_info()
            
            
    return jsonify(retorno), 200


def get_detalhes_mod(request:Request):
    # Recebe os dados do corpo da requisição (JSON)
    data = request.json
    # Extrai os atributos do corpo
    month = str(data.get("mes"))
    atendimento = "40"+str(data.get("atendimento"))

    # Valida se os atributos foram fornecidos
    if not month or not atendimento:
        return jsonify({"error": "Os atributos 'mes' e 'atendimento' são obrigatórios"}), 400
    
    try:
        # Carrega o arquivo CSV
        file = 'ganep_lar/orcamentos/data/detalhemod.csv'
        df = pd.read_csv(file, encoding='utf-8')

        # Filtra o DataFrame com base nos valores de month e atendimento
        df['MONTH'] = df['MONTH'].astype(str)
        df['SECADMISSION'] = df['SECADMISSION'].astype(str)
        filtro = (df['MONTH'] == month) & (df['SECADMISSION'] == atendimento)
        df_filtrado = df[filtro]

        # Verifica se há dados após a filtragem
        if df_filtrado.empty:
            return []

        dados = [DetalhesMod(**kwargs).__dict__() for index, kwargs in df_filtrado.iterrows()]

        return jsonify(dados), 200

    except FileNotFoundError:
        return {"error": f"Arquivo '{file}' não encontrado"}
    except KeyError as e:
        return {"error": f"Coluna não encontrada: {str(e)}"}
    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}


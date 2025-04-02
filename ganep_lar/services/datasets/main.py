from intercorrencias.main import load_and_insert_data as load_and_insert_intercorrencias
from mapa_atendimentos.main import load_and_insert_data as load_and_insert_mapa_atendimentos
from atendimentos_completo.main import load_and_insert_data as load_and_insert_atendimentos_completo
from ccids.main import load_and_insert_data as load_and_insert_ccids
from visitas.main import load_and_insert_data as load_and_insert_visitas
from orcamentos.main import load_and_insert_data as load_and_insert_orcamentos
from equipe.main import load_and_insert_data as load_and_insert_equipe

# Inserir dados de intercorrências no banco de dados
#load_and_insert_intercorrencias()

# # # Inserir dados de mapa de atendimentos no banco de dados
load_and_insert_mapa_atendimentos()

# # # Inserir dados de atendimentos completo no banco de dados
#load_and_insert_atendimentos_completo()

# # # Inserir dados de CCIDs no banco de dados
#load_and_insert_ccids()

# # # Inserir dados de visitas no banco de dados
#load_and_insert_visitas()

# # Inserir dados de orçamentos no banco de dados
#load_and_insert_orcamentos()

# # Inserir dados de equipe no banco de dados
#load_and_insert_equipe()

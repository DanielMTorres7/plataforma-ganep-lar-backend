from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["GanepLar"]



def update_atendimento(new_atendimento):
    """Atualiza um atendimento no banco de dados.
    
    Args:
        n_atendimento (int): Número do atendimento a ser atualizado
        new_atendimento (dict): Dicionário com os campos a serem atualizados
    """
    new_atendimento = Iatendimento_completo(**new_atendimento).__dict__()
    # delete NASCIMENTO para evitar erro de conversão de tipo
    for key in ['NASCIMENTO','PACIENTE','PRONTUARIO','SEXO','_id']:
        if key in new_atendimento:
            new_atendimento.pop(key)

    n_atendimento = new_atendimento["ATENDIMENTO"]
    n_prontuario = new_atendimento["PRONTUARIO"]
    colecao_prontuarios = db["prontuarios"]
    
    # Remove campos None/null para evitar sobrescrita indesejada
    
    # Constrói o operador $set dinamicamente para atualizar o subdocumento
    set_command = {}
    for field, value in new_atendimento.items():
        set_command[f"ATENDIMENTOS.{n_atendimento}.{field}"] = value
    
    # Executa a atualização
    result = colecao_prontuarios.update_one(
        {"PRONTUARIO": n_prontuario, f"ATENDIMENTOS.{n_atendimento}": {"$exists": True}},
        {"$set": set_command}
    )
    print(result.modified_count)
    
    return result.modified_count


from atendimentos_completo.models import Iatendimento_completo
resultado = db.atendimentos_completo.find_one({"ATENDIMENTO": 8})

update_atendimento(resultado)
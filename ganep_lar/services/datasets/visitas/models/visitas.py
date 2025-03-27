from utils.convert_value_utils import *

class Visita:
    def __init__(self, **kwargs) -> None:
        # Mês	Cod. Especialidade	Especialidade	Nome Comercial	Nr. Atendimento	Paciente	Profissional	Nome do Profissional	Nr. Registro	VISITCOUNT	N° Pacientes
        self.mes = convert_to_str(kwargs.get('Mês'))
        self.cod_especialidade = convert_to_int(kwargs.get('Cod. Especialidade'))
        self.especialidade = convert_to_str(kwargs.get('Especialidade'))
        self.nome_comercial = convert_to_str(kwargs.get('Nome Comercial'))
        self.nr_atendimento = convert_to_int(kwargs.get('Nr. Atendimento'))
        self.paciente = convert_to_str(kwargs.get('Paciente'))
        self.profissional = convert_to_int(kwargs.get('Profissional'))
        self.nome_profissional = convert_to_str(kwargs.get('Nome do Profissional'))
        self.nr_registro = convert_to_str(kwargs.get('Nr. Registro'))
        self.visitcount = convert_to_int(kwargs.get('VISITCOUNT'))
        
    def __dict__(self):
        return {
            "MES": self.mes,
            "COD_ESPECIALIDADE": self.cod_especialidade,
            "ESPECIALIDADE": self.especialidade,
            "NOME_COMERCIAL": self.nome_comercial,
            "NR_ATENDIMENTO": self.nr_atendimento,
            "PACIENTE": self.paciente,
            "PROFISSIONAL": self.profissional,
            "NOME_PROFISSIONAL": self.nome_profissional,
            "NR_REGISTRO": self.nr_registro,
            "VISITCOUNT": self.visitcount
        }
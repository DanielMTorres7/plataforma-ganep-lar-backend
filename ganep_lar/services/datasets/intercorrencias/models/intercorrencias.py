from utils.convert_value_utils import *

class IIntercorrencia:
    def __init__(self, **kwargs):
        self.id = convert_to_int(kwargs.get('ID'))
        self.origem = convert_to_str(kwargs.get('ORIGEM'))
        self.tipo = convert_to_str(kwargs.get('TIPO'))
        self.urgencia = convert_to_str(kwargs.get('URGENCIA'))
        self.classificacao = convert_to_str(kwargs.get('CLASSIFICACAO'))
        self.data_inicio = convert_to_date(kwargs.get('DATA_INICIO'))
        self.status = convert_to_str(kwargs.get('STATUS'))
        self.atendimento = convert_to_int(kwargs.get('ATENDIMENTO'))
        self.paciente = convert_to_str(kwargs.get('PACIENTE'))
        self.operadora = convert_to_str(kwargs.get('OPERADORA'))
        self.data_aph = convert_to_date(kwargs.get('DATA_APH'))
        self.alta = convert_to_date(kwargs.get('ALTA'))
        self.motivo_alta = convert_to_str(kwargs.get('MOTIVO_ALTA'))
        self.detalhe = convert_to_str(kwargs.get('DETALHE'))
        self.idqualyteam = convert_to_int(kwargs.get('IDQUALYTEAM'))
        self.nascimento = convert_to_date(kwargs.get('NASCIMENTO'))
        self.notificante = convert_to_str(kwargs.get('NOTIFICANTE'))
        self.modalidade = convert_to_str(kwargs.get('MODALIDADE'))
        """
        str -> AD | ID
        """


    def getAtt(self, att):
        return self.__dict__[att]
    
    def __dict__(self):
        return {
            'ID': self.id,
            'ORIGEM': self.origem,
            'TIPO': self.tipo,
            'URGENCIA': self.urgencia,
            'CLASSIFICACAO': self.classificacao,
            'DATA_INICIO': self.data_inicio,
            'STATUS': self.status,
            'ATENDIMENTO': self.atendimento,
            'PACIENTE': self.paciente,
            'OPERADORA': self.operadora,
            'DATA_APH': self.data_aph,
            'ALTA': self.alta,
            'MOTIVO_ALTA': self.motivo_alta,
            'DETALHE': self.detalhe
        }
    

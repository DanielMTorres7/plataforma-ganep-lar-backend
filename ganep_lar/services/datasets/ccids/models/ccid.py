from utils.convert_value_utils import *

class CCID:
    def __init__(self, **kwargs) -> None:
        self.competencia = convert_to_date(kwargs.get('COMPETENCIA'),format='%d/%m/%Y')
        self.cod_beneficiario = convert_to_str(kwargs.get('COD_BENEFICIARIO'))
        self.nome_paciente = convert_to_str(kwargs.get('NOME_PACIENTE'))
        # self.idade = convert_to_str(kwargs.get('IDADE'))
        self.sexo = convert_to_str(kwargs.get('SEXO'))
        """
        str -> Masculino | Feminino
        """
        self.prestador = convert_to_str(kwargs.get('PRESTADOR'))
        self.modalidade = convert_to_str(kwargs.get('MODALIDADE'))
        self.diagnostico = convert_to_str(kwargs.get('DIAGNOSTICO'))
        self.inicio_atendimento = convert_to_date(kwargs.get('INICIO_ATENDIMENTO'),format='%d/%m/%Y')
        self.data_ocorrencia = convert_to_date(kwargs.get('DATA_OCORRENCIA'),format='%d/%m/%Y')
        self.tipo_infeccao = convert_to_str(kwargs.get('TIPO_INFECCAO'))
        self.uso_dispositivo = convert_to_str(kwargs.get('USO_DISPOSITIVO'))
        self.uso_fralda = convert_to_bool(kwargs.get('USO_FRALDA'))
        self.uso_antibiotico = convert_to_bool(kwargs.get('USO_ANTIBIOTICO'))
        self.antibiotico = convert_to_str(kwargs.get('ANTIBIOTICO'))
        self.internacao = convert_to_bool(kwargs.get('INTERNACAO'))
        self.protocolo = convert_to_str(kwargs.get('PROTOCOLO'))
        self.cnu_tipo_infeccao = convert_to_str(kwargs.get('CNU_TIPO_INFECCAO'))
        self.operadora = convert_to_str(kwargs.get('OPERADORA'))
        
    def __dict__(self):
        return {
            'COMPETENCIA': self.competencia,
            'COD_BENEFICIARIO': self.cod_beneficiario,
            'NOME_PACIENTE': self.nome_paciente,
            'SEXO': self.sexo,
            'PRESTADOR': self.prestador,
            'MODALIDADE': self.modalidade,
            'DIAGNOSTICO': self.diagnostico,
            'INICIO_ATENDIMENTO': self.inicio_atendimento,
            'DATA_OCORRENCIA': self.data_ocorrencia,
            'TIPO_INFECCAO': self.tipo_infeccao,
            'USO_DISPOSITIVO': self.uso_dispositivo,
            'USO_FRALDA': self.uso_fralda,
            'USO_ANTIBIOTICO': self.uso_antibiotico,
            'ANTIBIOTICO': self.antibiotico,
            'INTERNACAO': self.internacao,
            'PROTOCOLO': self.protocolo,
            'CNU_TIPO_INFECCAO': self.cnu_tipo_infeccao,
            'OPERADORA': self.operadora
        }
from utils.convert_value_utils import *

class atendimento:
    def __init__(self, **kwargs) -> None: 
        self.id_operadora = convert_to_int(kwargs.get('ID_OPERADORA'))
        self.operadora = convert_to_str(kwargs.get('OPERADORA'))
        self.id_contrato = convert_to_int(kwargs.get('ID_CONTRATO'))
        self.contrato = convert_to_str(kwargs.get('CONTRATO'))
        self.prontuario = convert_to_int(kwargs.get('PRONTUARIO'))
        self.atendimento = convert_to_int(kwargs.get('ATENDIMENTO'))
        self.paciente = convert_to_str(kwargs.get('PACIENTE'))
        self.grupo = convert_to_str(kwargs.get('GRUPO')) 
        """
        str -> AD | ID
        """
        self.programa = convert_to_str(kwargs.get('PROGRAMA'))
        self.status = convert_to_str(kwargs.get('STATUS'))
        self.entrada = convert_to_date(kwargs.get('ENTRADA'))
        self.alta = convert_to_date(kwargs.get('ALTA'))
        self.motivo_alta = convert_to_str(kwargs.get('MOTIVO_ALTA'))
        self.previsao_alta = convert_to_date(kwargs.get('PREVISAO_ALTA'))
        self.data_registro = convert_to_date(kwargs.get('DATA_REGISTRO'))
        self.tipo = convert_to_str(kwargs.get('TIPO'))
        """
        str -> Novo | Retorno
        """
        self.origem = convert_to_str(kwargs.get('ORIGEM'))
        self.data_avaliacao = convert_to_date(kwargs.get('DATA_AVALIACAO'))
        self.data_orcamento = convert_to_date(kwargs.get('DATA_ORCAMENTO'))
        self.complexidade = convert_to_str(kwargs.get('COMPLEXIDADE'))
        self.complexidade_padrao = convert_to_str(kwargs.get('COMPL_PADRAO'))
        self.data_reprovado = convert_to_date(kwargs.get('DATA_REPROVADO'))
        self.motivo_reprovacao = convert_to_str(kwargs.get('MOTIVO_REPROVACAO'))
        self.liminar = convert_to_bool(kwargs.get('LIMINAR'))
        self.endereco = convert_to_str(kwargs.get('ENDERECO'))
        self.bairro = convert_to_str(kwargs.get('BAIRRO'))
        self.cidade = convert_to_str(kwargs.get('CIDADE'))
        self.estado = convert_to_str(kwargs.get('ESTADO'))
        self.cep = convert_to_cep(kwargs.get('CEP'))
        self.regiao = convert_to_str(kwargs.get('REGIAO'))
        self.grupo_cep = convert_to_str(kwargs.get('GRUPO_CEP'))
        self.nascimento = convert_to_date(kwargs.get('NASCIMENTO'))
        self.faixa_etaria = convert_to_str(kwargs.get('FAIXA_ETARIA'))
        """
        str -> 
            de 06 a 10 anos
            de 11 a 20 anos
            de 21 a 30 anos
            de 31 a 40 anos
            de 41 a 50 anos
            de 51 a 60 anos
            de 61 a 70 anos
            de 71 a 80 anos
            de 81 a 90 anos
            de 91 a 100 anos
            mais de 100 anos
        """
        self.sexo = convert_to_str(kwargs.get('SEXO'))
        """
        str -> Masculino | Feminino
        """
        self.carteirinha = convert_to_str(kwargs.get('CARTEIRINHA'))
        self.id_grupo_cid = convert_to_str(kwargs.get('ID_GRUPO_CID'))
        self.grupo_cid = convert_to_str(kwargs.get('GRUPO_CID'))
        self.cid10_1 = convert_to_str(kwargs.get('CID10_1'))
        self.cid10_2 = convert_to_str(kwargs.get('CID10_2'))
        self.cid10_3 = convert_to_str(kwargs.get('CID10_3'))
        self.cid10_4 = convert_to_str(kwargs.get('CID10_4'))
        self.cuidador = convert_to_str(kwargs.get('CUIDADOR'))
        self.parentesco = convert_to_str(kwargs.get('PARENTESCO'))
        self.score_braden = convert_to_int(kwargs.get('SCORE_BRADEN'))
        self.score_morse = convert_to_int(kwargs.get('SCORE_MORSE'))
        self.score_barthel = convert_to_int(kwargs.get('SCORE_BARTHEL'))
        self.score_humpty = convert_to_int(kwargs.get('SCORE_HUMPTY'))
        self.lesao_pressao = convert_to_bool(kwargs.get('LESAO_PRESSAO'))
        self.lesao_pressao_obs = convert_to_str(kwargs.get('LESAO_PRESSAO_OBS'))
        self.dispositivos = convert_to_bool(kwargs.get('DISPOSITIVOS'))
        self.dispositivos_obs = convert_to_str(kwargs.get('DISPOSITIVOS_OBS'))
        self.risco_queda = convert_to_bool(kwargs.get('RISCO_QUEDA'))
        self.risco_queda_obs = convert_to_str(kwargs.get('RISCO_QUEDA_OBS'))
        self.bcp_disfasia = convert_to_bool(kwargs.get('BCP_DISFASIA'))
        self.bcp_disfasia_obs = convert_to_str(kwargs.get('BCP_DISFASIA_OBS'))
        self.risco_nutri = convert_to_bool(kwargs.get('RISCO_NUTRI'))
        self.risco_nutri_obs = convert_to_str(kwargs.get('RISCO_NUTRI_OBS'))
        self.medicamentos = convert_to_bool(kwargs.get('MEDICAMENTOS'))
        self.medicamentos_obs = convert_to_str(kwargs.get('MEDICAMENTOS_OBS'))
        self.dap = convert_to_bool(kwargs.get('DAP'))
        self.dap_obs = convert_to_str(kwargs.get('DAP_OBS'))
        self.diabetes = convert_to_bool(kwargs.get('DIABETES'))
        self.diabetes_obs = convert_to_str(kwargs.get('DIABETES_OBS'))
        self.nucleo_conflito = convert_to_bool(kwargs.get('NUCLEO_CONFLITO'))
        
    def __dict__(self):
        return {
            'ID_OPERADORA': self.id_operadora,
            'OPERADORA': self.operadora,
            'ID_CONTRATO': self.id_contrato,
            'CONTRATO': self.contrato,
            'PRONTUARIO': self.prontuario,
            'ATENDIMENTO': self.atendimento,
            'PACIENTE': self.paciente,
            'GRUPO': self.grupo,
            'PROGRAMA': self.programa,
            'STATUS': self.status,
            'ENTRADA': self.entrada,
            'ALTA': self.alta,
            'MOTIVO_ALTA': self.motivo_alta,
            'PREVISAO_ALTA': self.previsao_alta,
            'DATA_REGISTRO': self.data_registro,
            'TIPO': self.tipo,
            'ORIGEM': self.origem,
            'DATA_AVALIACAO': self.data_avaliacao,
            'DATA_ORCAMENTO': self.data_orcamento,
            'COMPLEXIDADE': self.complexidade,
            'COMPL_PADRAO': self.complexidade_padrao,
            'DATA_REPROVADO': self.data_reprovado,
            'MOTIVO_REPROVACAO': self.motivo_reprovacao,
            'LIMINAR': self.liminar,
            'ENDERECO': self.endereco,
            'BAIRRO': self.bairro,
            'CIDADE': self.cidade,
            'ESTADO': self.estado,
            'CEP': self.cep,
            'REGIAO': self.regiao,
            'GRUPO_CEP': self.grupo_cep,
            'NASCIMENTO': self.nascimento,
            'FAIXA_ETARIA': self.faixa_etaria,
            'SEXO': self.sexo,
            'CARTEIRINHA': self.carteirinha,
            'ID_GRUPO_CID': self.id_grupo_cid,
            'GRUPO_CID': self.grupo_cid,
            'CID10_1': self.cid10_1,
            'CID10_2': self.cid10_2,
            'CID10_3': self.cid10_3,
            'CID10_4': self.cid10_4,
            'CUIDADOR': self.cuidador,
            'PARENTESCO': self.parentesco,
            'SCORE_BRADEN': self.score_braden,
            'SCORE_MORSE': self.score_morse,
            'SCORE_BARTHEL': self.score_barthel,
            'SCORE_HUMPTY': self.score_humpty,
            'LESAO_PRESSAO': self.lesao_pressao,
            'LESAO_PRESSAO_OBS': self.lesao_pressao_obs,
            'DISPOSITIVOS': self.dispositivos,
            'DISPOSITIVOS_OBS': self.dispositivos_obs,
            'RISCO_QUEDA': self.risco_queda,
            'RISCO_QUEDA_OBS': self.risco_queda_obs,
            'BCP_DISFASIA': self.bcp_disfasia,
            'BCP_DISFASIA_OBS': self.bcp_disfasia_obs,
            'RISCO_NUTRI': self.risco_nutri,
            'RISCO_NUTRI_OBS': self.risco_nutri_obs,
            'MEDICAMENTOS': self.medicamentos,
            'MEDICAMENTOS_OBS': self.medicamentos_obs,
            'DAP': self.dap,
            'DAP_OBS': self.dap_obs,
            'DIABETES': self.diabetes,
            'DIABETES_OBS': self.diabetes_obs,
            'NUCLEO_CONFLITO': self.nucleo_conflito
        }
        
    def getAtt(self, att):
        return self.__dict__[att]
    
    
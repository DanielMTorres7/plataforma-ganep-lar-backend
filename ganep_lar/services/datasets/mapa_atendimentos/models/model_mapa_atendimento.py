from utils.convert_value_utils import *

class ModelMapaAtendimento:
    # IDADE,CASE,MODALIDADE,ID_OPERADORA,OPERADORA,ID_CONTRATO,CONTRATO,PRONTUARIO,ATENDIMENTO,PACIENTE,GRUPO,PROGRAMA,STATUS,ENTRADA,ALTA,MOTIVO_ALTA,PREVISAO_ALTA,DATA_REGISTRO,TIPO,ORIGEM,DATA_AVALIACAO,DATA_ORCAMENTO,COMPLEXIDADE,COMPL_PADRAO,DATA_REPROVADO,MOTIVO_REPROVACAO,LIMINAR,ENDERECO,BAIRRO,CIDADE,ESTADO,CEP,REGIAO,GRUPO_CEP,NASCIMENTO,FAIXA_ETARIA,SEXO,IDADE,PONTOS,ESCORE_REHOSP,TEMPO,QUANDO,RECUSA,P. VINCULO,PV CLASS
    def __init__(self, **kwargs):
        # self.idade = convert_to_str(kwargs.get('IDADE'))
        self.case = convert_to_str(kwargs.get('CASE'))
        self.modalidade = convert_to_str(kwargs.get('MODALIDADE'))
        self.id_operadora = convert_to_int(kwargs.get('ID_OPERADORA'))
        self.operadora = convert_to_str(kwargs.get('OPERADORA'))
        self.id_contrato = convert_to_int(kwargs.get('ID_CONTRATO'))
        self.contrato = convert_to_str(kwargs.get('CONTRATO'))
        self.prontuario = convert_to_int(kwargs.get('PRONTUARIO'))
        self.atendimento = convert_to_int(kwargs.get('ATENDIMENTO'))
        self.paciente = convert_to_str(kwargs.get('PACIENTE'))
        self.grupo = convert_to_str(kwargs.get('GRUPO'))
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
        self.pontos = convert_to_int(kwargs.get('PONTOS'))
        self.escore_rehosp = convert_to_str(kwargs.get('ESCORE_REHOSP'))
        self.tempo = convert_to_float(kwargs.get('TEMPO'))
        self.quando = convert_to_str(kwargs.get('QUANDO'))
        self.recusa = convert_to_date(kwargs.get('RECUSA'))
        self.p_vinculo = convert_to_date(kwargs.get('P. VINCULO'))
        self.pv_class = convert_to_str(kwargs.get('PV CLASS'))
        """
        str -> Retorno | Realizado
        """

    def __dict__(self):
        return {
            'CASE': self.case,
            'MODALIDADE': self.modalidade,
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
            'PONTOS': self.pontos,
            'ESCORE_REHOSP': self.escore_rehosp,
            'TEMPO': self.tempo,
            'QUANDO': self.quando,
            'RECUSA': self.recusa,
            'P. VINCULO': self.p_vinculo,
            'PV CLASS': self.pv_class,
        }
        
from utils.convert_value_utils import *

class IOrcamento:
    def __init__(self, **kwargs):
        # ATENDIMENTO	ID_ORCAMENTO	ID_COMPLEXIDADE	COMPLEXIDADE	DATA_INICIO	DATA_FINAL	DURACAO	RECEITA	CUSTO	RECEITA_MAT	RECEITA_EQP	RECEITA_UTI	RECEITA_MOD	RECEITA_PRC	RECEITA_EXM	RECEITA_DIA	CUSTO_MAT	CUSTO_EQP	CUSTO_UTI	CUSTO_MOD	CUSTO_PRC	CUSTO_EXM	CUSTO_DIA	CUSTO_TAX	OPERADORA
        self.atendimento = kwargs.get("ATENDIMENTO")
        self.id_orcamento = kwargs.get("ID_ORCAMENTO")
        self.id_complexidade = kwargs.get("ID_COMPLEXIDADE")
        self.complexidade = kwargs.get("COMPLEXIDADE")
        self.data_inicio = convert_to_date(kwargs.get("DATA_INICIO"))
        self.data_final = convert_to_date(kwargs.get("DATA_FINAL"))
        self.duracao = convert_to_int(kwargs.get("DURACAO"))
        self.receita = convert_to_float(kwargs.get("RECEITA"))
        self.custo = convert_to_float(kwargs.get("CUSTO"))
        self.receita_mat = convert_to_float(kwargs.get("RECEITA_MAT"))
        self.receita_eqp = convert_to_float(kwargs.get("RECEITA_EQP"))
        self.receita_uti = convert_to_float(kwargs.get("RECEITA_UTI"))
        self.receita_mod = convert_to_float(kwargs.get("RECEITA_MOD"))
        self.receita_prc = convert_to_float(kwargs.get("RECEITA_PRC"))
        self.receita_exm = convert_to_float(kwargs.get("RECEITA_EXM"))
        self.receita_dia = convert_to_float(kwargs.get("RECEITA_DIA"))
        self.custo_mat = convert_to_float(kwargs.get("CUSTO_MAT"))
        self.custo_eqp = convert_to_float(kwargs.get("CUSTO_EQP"))
        self.custo_uti = convert_to_float(kwargs.get("CUSTO_UTI"))
        self.custo_mod = convert_to_float(kwargs.get("CUSTO_MOD"))
        self.custo_prc = convert_to_float(kwargs.get("CUSTO_PRC"))
        self.custo_exm = convert_to_float(kwargs.get("CUSTO_EXM"))
        self.custo_dia = convert_to_float(kwargs.get("CUSTO_DIA"))
        self.custo_tax = convert_to_float(kwargs.get("CUSTO_TAX"))
        self.operadora = kwargs.get("OPERADORA")
    
    def __dict__(self):
        return {
            'ATENDIMENTO': self.atendimento,
            'ID_ORCAMENTO': self.id_orcamento,
            'ID_COMPLEXIDADE': self.id_complexidade,
            'COMPLEXIDADE': self.complexidade,
            'DATA_INICIO': self.data_inicio,
            'DATA_FINAL': self.data_final, 
            'DURACAO': self.duracao,
            'RECEITA': self.receita,
            'CUSTO': self.custo,
            'RECEITA_MAT': self.receita_mat,
            'RECEITA_EQP': self.receita_eqp,
            'RECEITA_UTI': self.receita_uti,
            'RECEITA_MOD': self.receita_mod,
            'RECEITA_PRC': self.receita_prc,
            'RECEITA_EXM': self.receita_exm,
            'RECEITA_DIA': self.receita_dia,
            'CUSTO_MAT': self.custo_mat,
            'CUSTO_EQP': self.custo_eqp,
            'CUSTO_UTI': self.custo_uti,
            'CUSTO_MOD': self.custo_mod,
            'CUSTO_PRC': self.custo_prc,
            'CUSTO_EXM': self.custo_exm,
            'CUSTO_DIA': self.custo_dia,
            'CUSTO_TAX': self.custo_tax,
            'OPERADORA': self.operadora
        }
    

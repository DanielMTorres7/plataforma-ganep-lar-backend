def colorir_mc(custo, receita, v1=30.5, v2=30):
    if receita == 0:
        saida = 0
    elif v1 == 0:
        saida = ((receita - custo) / receita * 100)
    elif (receita - custo) / receita * 100 >= v1:
        saida = ((receita - custo) / receita * 100)
    elif (receita - custo) / receita * 100 >= v2:
        saida = ((receita - custo) / receita * 100)
    else:
        saida = ((receita - custo) / receita * 100)
    return saida

def formatar_thin(entrada):
    saida = (entrada)
    return saida

def colorir_prt(custo, custotot, v1, v2):
    if custotot == 0:
        saida = 0
    elif v1 == 0:
        saida = (custo / custotot * 100)
    elif custo / custotot * 100 <= v1:
        saida = (custo / custotot * 100)
    elif custo / custotot * 100 <= v2:
        saida = (custo / custotot * 100)
    else:
        saida = (custo / custotot * 100)
    return saida


class DfInfos:
    def __init__(self, df, title: str):
        self._df = df
        self.title = title
        self.children = []
    
    def get_info(self):
        VLORCADO: float = self._df['VLORCADO'].sum()
        VLCSTDIA: float = self._df['VLCSTDIA'].sum()
        VLORCDIA: float = self._df['VLORCDIA'].sum()
        VLCSTMOD: float = self._df['VLCSTMOD'].sum()
        VLORCMOD: float = self._df['VLORCMOD'].sum()
        VLCSTMAT: float = self._df['VLCSTMAT'].sum()
        VLORCMAT: float = self._df['VLORCMAT'].sum()
        VLCSTEQG: float = self._df['VLCSTEQG'].sum()
        VLORCEQG: float = self._df['VLORCEQG'].sum()
        VLCSTOUT: float = self._df['VLCSTOUT'].sum()
        VLORCOUT: float = self._df['VLORCOUT'].sum()
        VLTOTCSTMOD: float = self._df['VLTOTCSTMOD'].sum()
        VLTOTCSTMAT: float = self._df['VLTOTCSTMAT'].sum()
        VLTOTCSTEQG: float = self._df['VLTOTCSTEQG'].sum()
        VLTOTCSTOUT: float = self._df['VLTOTCSTOUT'].sum()
        VLCSTIMP: float = self._df['VLCSTIMP'].sum()
        VLCSTIMP: float = self._df['VLCSTIMP'].sum()
        VLCUSTO: float = self._df['VLCUSTO'].sum()
        CUSTONAOORCADO: float = self._df['CUSTONAOORCADO'].sum()
        RECEITANAOREALIZADA: float = self._df['RECEITANAOREALIZADA'].sum()
        SECADMISSION: list = len(self._df['SECADMISSION'].unique())

        self.orcado = round(VLORCADO,2)
        self.custo = round(VLCUSTO,2)
        self.custo_nao_orcado = round(CUSTONAOORCADO,2)
        self.receita_nao_realizada = round(RECEITANAOREALIZADA,2)
        self.atendimentos = round(SECADMISSION,2)
        self.ticket_medio = round((VLORCADO/SECADMISSION),2)
        self.margem_contribuicao_geral = round(colorir_mc(self.custo, VLORCADO),2)
        self.margem_contribuicao_dia = round(colorir_mc(VLCSTDIA, VLORCDIA),2)
        self.margem_contribuicao_mod = round(colorir_mc(VLCSTMOD, VLORCMOD),2)
        self.margem_contribuicao_mat = round(colorir_mc(VLCSTMAT, VLORCMAT),2)
        self.margem_contribuicao_eqg = round(colorir_mc(VLCSTEQG, VLORCEQG),2)
        self.margem_contribuicao_out = round(colorir_mc(VLCSTOUT, VLORCOUT),2)
        self.margem_participacao_dia = round(formatar_thin((VLORCDIA - VLCSTDIA)),2)
        self.margem_participacao_mod = round(formatar_thin((VLORCMOD - VLCSTMOD)),2)
        self.margem_participacao_mat = round(formatar_thin((VLORCMAT - VLCSTMAT)),2)
        self.margem_participacao_eqg = round(formatar_thin((VLORCEQG - VLCSTEQG)),2)
        self.margem_participacao_out = round(formatar_thin((VLORCOUT - VLCSTOUT)),2)
        self.margem_participacao_imp = round(formatar_thin((-VLCSTIMP)),2)
        self.custo_receita_mod = round(colorir_prt(VLTOTCSTMOD, VLORCADO, 40,42),2)
        self.custo_receita_mat = round(colorir_prt(VLTOTCSTMAT, VLORCADO, 12,13),2)
        self.custo_receita_eqg = round(colorir_prt(VLTOTCSTEQG, VLORCADO, 3.5,4),2)
        self.custo_receita_out = round(colorir_prt(VLTOTCSTOUT, VLORCADO, 0,0),2)
        self.custo_receita_imp = round(colorir_prt(VLCSTIMP, VLORCADO, 0, 0),2)


        dict_info = self.__dict__()
        return dict_info
    
    def add_child(self, child):
        self.children.append(child)
    
    def __dict__(self):
        return {
            'title': self.title,
            'orcado': self.orcado,
            'custo': self.custo,
            'custo_nao_orcado': self.custo_nao_orcado,
            'receita_nao_realizada': self.receita_nao_realizada,
            'atendimentos': self.atendimentos,
            'ticket_medio': self.ticket_medio,
            'margem_contribuicao_geral': self.margem_contribuicao_geral,
            'margem_contribuicao_dia': self.margem_contribuicao_dia,
            'margem_contribuicao_mod': self.margem_contribuicao_mod,
            'margem_contribuicao_mat': self.margem_contribuicao_mat,
            'margem_contribuicao_eqg': self.margem_contribuicao_eqg,
            'margem_contribuicao_out': self.margem_contribuicao_out,
            'margem_participacao_dia': self.margem_participacao_dia,
            'margem_participacao_mod': self.margem_participacao_mod,
            'margem_participacao_mat': self.margem_participacao_mat,
            'margem_participacao_eqg': self.margem_participacao_eqg,
            'margem_participacao_out': self.margem_participacao_out,
            'margem_participacao_imp': self.margem_participacao_imp,
            'custo_receita_mod': self.custo_receita_mod,
            'custo_receita_mat': self.custo_receita_mat,
            'custo_receita_eqg': self.custo_receita_eqg,
            'custo_receita_out': self.custo_receita_out,
            'custo_receita_imp': self.custo_receita_imp,
            'children': self.children
        }
        
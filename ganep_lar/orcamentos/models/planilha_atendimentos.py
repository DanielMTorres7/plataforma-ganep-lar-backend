from .atendimento import Atendimento

class PlanilhaAtendimentos:
    def __init__(self, atendimento:Atendimento):
        self.atendimento = self.DadosAtendimento(atendimento)
        self.totais = self.DadosTotais(atendimento)
        self.diarias_pacotes = self.DadosDiariasPacotes(atendimento)
        self.mao_obra_direta = self.DadosMod(atendimento)
        self.materias_medicamentos = self.DadosMat(atendimento)
        self.equipamentos_gases = self.DadosEqg(atendimento)
        self.outros_insumos = self.DadosOut(atendimento)
        self.detalhamento_grupos = self.DadosDetalhes(atendimento)

    class DadosAtendimento:
        def __init__(self, atendimento:Atendimento):
            self.mes = atendimento.MONTH
            self.atendimento = atendimento.IDADMISSION
            self.paciente = atendimento.PATIENTNAME
            self.admissao = atendimento.CHECKINDATE
            self.alta = atendimento.CHECKOUTDATE
        
        def __dict__(self):
            return {
                "mes": self.mes,
                "atendimento": self.atendimento,
                "paciente": self.paciente,
                "admissao": self.admissao,
                "alta": str(self.alta)
            }
    
    class DadosTotais:
        def __init__(self, atendimento:Atendimento):
            self.nao_orcado = to_float(atendimento.CUSTONAOORCADO)
            self.nao_programado = to_float(atendimento.RECEITANAOREALIZADA)
            self.total_orcado = to_float(atendimento.VLORCADO)
            self.custo_total = to_float(atendimento.VLCUSTO)
            self.margem_contribuicao = to_float(atendimento.MCORCADO)
        
        def __dict__(self):
            return {
                "nao_orcado": self.nao_orcado,
                "nao_programado": self.nao_programado,
                "total_orcado": self.total_orcado,
                "custo_total": self.custo_total,
                "margem_contribuicao": self.margem_contribuicao
            }
            
    class DadosDiariasPacotes:
        def __init__(self, atendimento:Atendimento):
            self.orcado_diarias = to_float(atendimento.VLORCDIA)
            self.custo_diarias = to_float(atendimento.VLCSTDIA)
            self.margem_contribuicao = to_float(atendimento.MCORCDIA)

        def __dict__(self):
            return {
                "orcado_diarias": self.orcado_diarias,
                "custo_diarias": self.custo_diarias,
                "margem_contribuicao": self.margem_contribuicao
            }
    
    class DadosMod:
        def __init__(self, atendimento:Atendimento):
            self.orcado_mod = to_float(atendimento.VLORCMOD)
            self.custo_aberto = to_float(atendimento.VLCSTMOD)
            self.custo_total = to_float(atendimento.VLCSTMOD)
            self.margem_contribuicao = to_float(atendimento.MCORCMOD)
            self.custo_receita = to_float(atendimento.VLTOTCSTMOD)

        def __dict__(self):
            return {
                "orcado_mod": self.orcado_mod,
                "custo_aberto": self.custo_aberto,
                "custo_total": self.custo_total,
                "margem_contribuicao": self.margem_contribuicao,
                "custo_receita": self.custo_receita
            }

    class DadosMat:
        def __init__(self, atendimento:Atendimento):
            self.orcado_mat = to_float(atendimento.VLORCMAT)
            self.custo_aberto = to_float(atendimento.VLCSTMAT)
            self.custo_total = to_float(atendimento.VLCSTMAT)
            self.margem_contribuicao = to_float(atendimento.MCORCMAT)
            self.custo_receita = to_float(atendimento.VLTOTCSTMAT)

        def __dict__(self):
            return {
                "orcado_mat": self.orcado_mat,
                "custo_aberto": self.custo_aberto,
                "custo_total": self.custo_total,
                "margem_contribuicao": self.margem_contribuicao,
                "custo_receita": self.custo_receita
            }

    class DadosEqg:
        def __init__(self, atendimento:Atendimento):
            self.orcado_eqg = to_float(atendimento.VLORCEQG)
            self.custo_aberto = to_float(atendimento.VLCSTEQG)
            self.custo_total = to_float(atendimento.VLCSTEQG)
            self.margem_contribuicao = to_float(atendimento.MCORCEQG)
            self.custo_receita = to_float(atendimento.VLTOTCSTEQG)
        
        def __dict__(self):
            return {
                "orcado_eqg": self.orcado_eqg,
                "custo_aberto": self.custo_aberto,
                "custo_total": self.custo_total,
                "margem_contribuicao": self.margem_contribuicao,
                "custo_receita": self.custo_receita
            }
    
    class DadosOut:
        def __init__(self, atendimento:Atendimento):
            self.orcado_out = to_float(atendimento.VLORCOUT)
            self.custo_aberto = to_float(atendimento.VLCSTOUT)
            self.custo_total = to_float(atendimento.VLCSTOUT)
            self.margem_contribuicao = to_float(atendimento.MCORCOUT)
            self.custo_receita = to_float(atendimento.VLTOTCSTOUT)
            self.custo_impostos = to_float(atendimento.VLCSTIMP)
        
        def __dict__(self):
            return {
                "orcado_out": self.orcado_out,
                "custo_aberto": self.custo_aberto,
                "custo_total": self.custo_total,
                "margem_contribuicao": self.margem_contribuicao,
                "custo_receita": self.custo_receita,
                "custo_impostos": self.custo_impostos
            }
    
    class DadosDetalhes:
        def __init__(self, atendimento:Atendimento):
            self.regional = atendimento.REGIONAL
            self.servico = atendimento.ADMISSIONTYPENAME
            self.empresa = atendimento.ENTERPRISENAME
            self.unidade = atendimento.SEDE
            self.convenio = atendimento.ENTERPRISENAME
            self.carteira = atendimento.SECNTICARTEIRA
            self.contrato = atendimento.CONTRACTNAME
        
        def __dict__(self):
            return {
                "regional": self.regional,
                "servico": self.servico,
                "empresa": self.empresa,
                "unidade": self.unidade,
                "convenio": self.convenio,
                "carteira": self.carteira,
                "contrato": self.contrato
            }

    def __dict__(self):
        return {
            "atendimento": self.atendimento.__dict__(),
            "totais": self.totais.__dict__(),
            "diarias_pacotes": self.diarias_pacotes.__dict__(),
            "mao_obra_direta": self.mao_obra_direta.__dict__(),
            "materias_medicamentos": self.materias_medicamentos.__dict__(),
            "equipamentos_gases": self.equipamentos_gases.__dict__(),
            "outros_insumos": self.outros_insumos.__dict__(),
            "detalhamento_grupos": self.detalhamento_grupos.__dict__()
        }
    
def to_float(value):
    try:
        # Remove os pontos (separadores de milhares)
        value = str(value).replace(',', '.')
        # Converte para float e arredonda para 2 casas decimais
        value = round(float(value),2)
        return ("{:.2f}".format(value)).replace('.', ',')
    except Exception as e:
        print(f"Erro ao converter valor: {e}")
        return value
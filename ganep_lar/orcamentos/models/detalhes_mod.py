class DetalhesMod:
    def __init__(self, **kwargs):
        # "SECREGIONAL","SECADMISSIONTYPE","SECIDCORPORATION","SECNTICARTEIRA","SECIDENTERPRISE","SECIDCONTRACT","REGIONAL","ADMISSIONTYPENAME","SECZONECODE","CORPORATIONNAME","ZONECODENAME","NTICARTEIRANAME","ENTERPRISENAME","CONTRACTNAME","PATIENTNAME","CHECKINDATE","CHECKOUTDATE","ZIPZONE","CITY","SECADMISSION","SECPROFESSIONAL","MONTH","ORIGEM","SPECIALITYNAME","AGENDASTARTDATE","AGENDAENDDATE","PROFPROVIDERNAME","PROFESSIONALNAME","REGISTRYNUMBER","CHARGE","PAY","SHIFT","REALIZED","MANUAL","SHORTSPECIALITY","QUANTITY","BASE","BONUS","TAXAADM","INSS","FGTS","PTRABALHISTA","TRANSP","BENEFICIOS","TOTAL","PRECOMANUAL"
        self.origem = str(kwargs.get('ORIGEM', "N/A"))
        self.especialidade = str(kwargs.get('SPECIALITYNAME', "N/A"))
        self.custo_total = str(kwargs.get('TOTAL', "N/A"))
        self.agendar_de = str(kwargs.get('AGENDASTARTDATE', "N/A"))
        self.agendar_ate = str(kwargs.get('AGENDAENDDATE', "N/A"))
        self.profissional = str(kwargs.get('PROFPROVIDERNAME', "N/A"))
        self.conselho = str(kwargs.get('REGISTRYNUMBER', "N/A"))
        self.empresa = str(kwargs.get('ENTERPRISENAME', "N/A"))
        self.qtde = str(kwargs.get('QUANTITY', "N/A"))
        self.base = str(kwargs.get('BASE', "N/A"))
        self.bonus = str(kwargs.get('BONUS', "N/A"))
        self.tx_adm = str(kwargs.get('TAXAADM', "N/A"))
        self.inss = str(kwargs.get('INSS', "N/A"))
        self.fgts = str(kwargs.get('FGTS', "N/A"))
        self.provisoes = str(kwargs.get('PTRABALHISTA', "N/A"))
        self.transporte = str(kwargs.get('TRANSP', "N/A"))
        self.beneficios = str(kwargs.get('BENEFICIOS', "N/A"))
        self.editado = str(kwargs.get('TOTAL', "N/A"))
        self.cobrar = str(kwargs.get('CHARGE', "N/A"))
        self.pagar = str(kwargs.get('PAY', "N/A"))
        self.plantao = str(kwargs.get('SHIFT', "N/A"))
        self.realizado = str(kwargs.get('REALIZED', "N/A"))
        self.manual = str(kwargs.get('MANUAL', "N/A"))
    
    def __dict__(self):
        return {
            "origem": self.origem,
            "especialidade": self.especialidade,
            "custo_total": self.custo_total,
            "agendar_de": self.agendar_de,
            "agendar_ate": self.agendar_ate,
            "profissional": self.profissional,
            "conselho": self.conselho,
            "empresa": self.empresa,
            "qtde": self.qtde,
            "base": self.base,
            "bonus": self.bonus,
            "tx_adm": self.tx_adm,
            "inss": self.inss,
            "fgts": self.fgts,
            "provisoes": self.provisoes,
            "transporte": self.transporte,
            "beneficios": self.beneficios,
            "editado": self.editado,
            "cobrar": self.cobrar,
            "pagar": self.pagar,
            "plantao": self.plantao,
            "realizado": self.realizado,
            "manual": self.manual
        }
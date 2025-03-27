from utils.convert_value_utils import *

class IEquipe:
    def __init__(self, **kwargs):
        # IDADMISSION	PATIENTNAME	SERVICO_SOCIAL	TEC_ENFERMAGEM	ESTOMA_PROFISSIONAL	ESTOMA_FREQUENCIA	ENF_PROFISSIONAL	ENF_FREQUENCIA	MED_PROFISSIONAL	MED_FREQUENCIA	FISIO_PROFISSIONAL	FISIO_FREQUENCIA	NUTRI_PROFISSIONAL	NUTRI_FREQUENCIA	FONO_PROFISSIONAL	FONO_FREQUENCIA	TO_PROFISSIONAL	TO_FREQUENCIA	PSICO_PROFISSIONAL	PSICO_FREQUENCIA
        self.id_admission = convert_to_int(kwargs.get("IDADMISSION"))
        self.patient_name = kwargs.get("PATIENTNAME")
        self.servico_social = kwargs.get("SERVICO_SOCIAL")
        self.tec_enfermagem = kwargs.get("TEC_ENFERMAGEM")
        self.estoma_profissional = kwargs.get("ESTOMA_PROFISSIONAL")
        self.estoma_frequencia = kwargs.get("ESTOMA_FREQUENCIA")
        self.enf_profissional = kwargs.get("ENF_PROFISSIONAL")
        self.enf_frequencia = kwargs.get("ENF_FREQUENCIA")
        self.med_profissional = kwargs.get("MED_PROFISSIONAL")
        self.med_frequencia = kwargs.get("MED_FREQUENCIA")
        self.fisio_profissional = kwargs.get("FISIO_PROFISSIONAL")
        self.fisio_frequencia = kwargs.get("FISIO_FREQUENCIA")
        self.nutri_profissional = kwargs.get("NUTRI_PROFISSIONAL")
        self.nutri_frequencia = kwargs.get("NUTRI_FREQUENCIA")
        self.fono_profissional = kwargs.get("FONO_PROFISSIONAL")
        self.fono_frequencia = kwargs.get("FONO_FREQUENCIA")
        self.to_profissional = kwargs.get("TO_PROFISSIONAL")
        self.to_frequencia = kwargs.get("TO_FREQUENCIA")
        self.psico_profissional = kwargs.get("PSICO_PROFISSIONAL")
        self.psico_frequencia = kwargs.get("PSICO_FREQUENCIA")

    def __dict__(self):
        return {
            'ATENDIMENTO': self.id_admission,
            'PATIENTNAME': self.patient_name,
            'SERVICO_SOCIAL': self.servico_social,
            'TEC_ENFERMAGEM': self.tec_enfermagem,
            'ESTOMA_PROFISSIONAL': self.estoma_profissional,
            'ESTOMA_FREQUENCIA': self.estoma_frequencia,
            'ENF_PROFISSIONAL': self.enf_profissional,
            'ENF_FREQUENCIA': self.enf_frequencia,
            'MED_PROFISSIONAL': self.med_profissional,
            'MED_FREQUENCIA': self.med_frequencia,
            'FISIO_PROFISSIONAL': self.fisio_profissional,
            'FISIO_FREQUENCIA': self.fisio_frequencia,
            'NUTRI_PROFISSIONAL': self.nutri_profissional,
            'NUTRI_FREQUENCIA': self.nutri_frequencia,
            'FONO_PROFISSIONAL': self.fono_profissional,
            'FONO_FREQUENCIA': self.fono_frequencia,
            'TO_PROFISSIONAL': self.to_profissional,
            'TO_FREQUENCIA': self.to_frequencia,
            'PSICO_PROFISSIONAL': self.psico_profissional,
            'PSICO_FREQUENCIA': self.psico_frequencia
        }
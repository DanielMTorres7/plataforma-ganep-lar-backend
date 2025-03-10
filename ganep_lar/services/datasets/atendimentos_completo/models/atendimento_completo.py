from ..models.atendimentos import atendimento
from utils.convert_value_utils import *

class Iatendimento_completo(atendimento):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nucleo_conflito_obs = convert_to_str(kwargs.get('NUCLEO_CONFLITO_OBS'))
        self.hosp_origem = convert_to_str(kwargs.get('HOSP_ORIGEM'))
        self.hosp_destino = convert_to_str(kwargs.get('HOSP_DESTINO'))
        self.class_lesoes = convert_to_str(kwargs.get('CLASS_LESOES'))
        self.cvd = convert_to_bool(kwargs.get('CVD'))
        self.cva = convert_to_bool(kwargs.get('CVA'))
        self.picc = convert_to_bool(kwargs.get('PICC'))
        self.gtt = convert_to_bool(kwargs.get('GTT'))
        self.tqt = convert_to_bool(kwargs.get('TQT'))
        self.sne = convert_to_bool(kwargs.get('SNE'))

    def __dict__(self):
        return {
            **super().__dict__(),
            'NUCLEO_CONFLITO_OBS': self.nucleo_conflito_obs,
            'HOSP_ORIGEM': self.hosp_origem,
            'HOSP_DESTINO': self.hosp_destino,
            'CLASS_LESOES': self.class_lesoes,
            'CVD': self.cvd,
            'CVA': self.cva,
            'PICC': self.picc,
            'GTT': self.gtt,
            'TQT': self.tqt,
            'SNE': self.sne
        }

    
            
        
        


import pandas as pd
from datetime import datetime

def convert_to_date(value: str, format='%d/%m/%Y %H:%M', errors='coerce') -> datetime:
    if isinstance(value, datetime):
        return value
    try:
        return datetime.strptime(value, format)
    except (ValueError, TypeError):
        if errors == 'coerce':
            return None
        else:
            raise

def convert_to_int(value:str, errors='coerce') -> int:
    if type(value) == int:
        return value
    # Converte a coluna para inteiro
    converted_value = str(value).replace('.', '')
    try:
        return int(converted_value)
    except ValueError:
        if errors == 'coerce':
            return None
        else:
            raise

def convert_to_str(value:str) -> str:
    if pd.isna(value) or value is None:
        return ''
    
    if str(value) == '.':
        return ''
    
    if type(value) == str:
        return value
    
    # se o value for nan ou None, retorna vazio
    if pd.isna(value) or value is None:
        return ''
    
    return str(value)

def convert_to_float(value:str, errors='coerce') -> float:
    if type(value) == float:
        return
    if pd.isna(value) or value is None:
        return
    value = str(value)
    
    # Valores podem ser separados por , para decimais e . para milhares ou . para decimais
    # Se o valor contiver somente um ponto, ele é considerado como separador de decimais
    if value.count('.') == 1 and value.count(',') == 0:
        value = value.replace('.', ',')
    # Se o valor contiver mais de um ponto, ele é considerado como separador de milhares
    elif value.count('.') > 1:
        value = value.replace('.', '')
    # Se o valor contiver uma vírgula, ela é considerada como separador de decimais
    if value.count(',') == 1:
        value = value.replace(',', '.')
    # Se o valor contiver um ponto e uma vírgula depois do ponto, a vírgula é considerada como separador de decimais
    if value.count('.') == 1 and value.count(',') == 1 and value.index(',') > value.index('.'):
        value = value.replace('.', '').replace(',', '.')
    # Se o valor contiver um ponto e uma vírgula antes do ponto, o ponto é considerado como separador de decimais
    if value.count('.') == 1 and value.count(',') == 1 and value.index(',') < value.index('.'):
        value = value.replace(',', '')

    return pd.to_numeric(value, errors=errors)

def convert_to_bool(value:str) -> bool:
    if type(value) == bool:
        return
    value = str(value).lower()
    if value == 'sim' or value == 's' or value == '1':
        return True
    return False

def convert_to_cep(value:str) -> str:
    return str(value).replace('-', '')


__all__ = ['convert_to_date', 'convert_to_int', 'convert_to_str', 'convert_to_float', 'convert_to_bool', 'convert_to_cep']
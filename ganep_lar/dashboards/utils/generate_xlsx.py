from flask import Flask, send_file
from openpyxl import Workbook
import io

def download_xlsx(prontuarios: list[object]):
    # Cria um novo workbook e adiciona uma planilha
    wb = Workbook()
    ws = wb.active
    ws.title = "Prontuários"

    # Adiciona os dados à planilha
    ws.append([
        'Paciente',
        'Prontuário',
        'Nascimento',
    ])
    for prontuario in prontuarios:
        ws.append([
            prontuario['PACIENTE'],
            prontuario['PRONTUARIO'],
            prontuario['NASCIMENTO'],
        ])

    
    # Salva o workbook em um buffer de memória
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    # Retorna o arquivo para o cliente
    return send_file(
        buffer,
        as_attachment=True,
        download_name='dados.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
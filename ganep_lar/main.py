from config import SECRET_KEY, FIREBASE_LOGIN_URL, SECRET_KEY
import services.firebase.main

import locale
import datetime
import requests
import jwt

from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps


app = Flask(__name__)
CORS(app)

roles = {}
roles['admin'] = [
    'dashboards', 
    'dashboards-lpp', 
    'dashboards-lpp:read',
    'dashboards-hospitalizacoes',
    'dashboards-hospitalizacoes:read',
    'dashboards-dispositivos',
    'dashboards-dispositivos:read',
    'dashboards-movimentacoes',
    'dashboards-movimentacoes:read',
    'dashboards-infeccoes',
    'dashboards-infeccoes:read',
    'paineis',
    'paineis-gestaorisco',
    'paineis-gestaorisco:read',
    'orcamentos',
    'orcamentos:read',
    'produtosconvenio',
    'produtosconvenio:read',
    'detalhesmod',
    'detalhesmod:read'
]
roles['moderator'] = [].extend(roles['admin'])


def token_required(required_permissions=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')

            if not token:
                return jsonify({'message': 'Token is missing!'}), 403

            try:
                payload = jwt.decode(token.split(' ')[1], SECRET_KEY, algorithms=['HS256'])
                request.user = payload
            except:
                return jsonify({'message': 'Token is invalid!'}), 403

            # Verifica se o usuário é admin ou moderator
            user_role = payload.get('role')
            if user_role not in roles:
                return jsonify({'message': 'Unauthorized: Role required!'}), 403
            

            # Caso contrário, verifica as permissões
            if required_permissions:
                user_permissions = payload.get('permissions', [])
                user_permissions.extend(roles[user_role])
                print(user_permissions)
                print(required_permissions)
                for permission in required_permissions:
                    if permission not in user_permissions:
                        return jsonify({'message': 'Unauthorized: Permission required!'}), 403

            return f(*args, **kwargs)
        return decorated
    return decorator

@app.route('/api/login', methods=['POST'])
def c_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400

    # Autenticação com o Firebase
    try:
        response = requests.post(FIREBASE_LOGIN_URL, json={
            'email': email,
            'password': password,
            'returnSecureToken': True
        })
        response_data = response.json()

        if 'error' in response_data:
            return jsonify({'error': response_data['error']['message']}), 401

        # Dados do usuário autenticado
        uid = response_data['localId']
        id_token = response_data['idToken']

        # Crie um JWT personalizado
        payload = {
            'uid': uid,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10),
            'email': email,
            'role': 'admin',
            'permissions': []
        }
        custom_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'token': custom_token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/dashboards/lpp", methods=["POST"])
@token_required(required_permissions=["dashboards", "dashboards-lpp", "dashboards-lpp:read"])
def dashslpp():
    from dashboards.lpp.main import get_data
    return get_data(request)


@app.route("/dashboards/hospitalizacoes", methods=["POST"])
@token_required(required_permissions=["dashboards", "dashboards-hospitalizacoes", "dashboards-hospitalizacoes:read"])
def dashshospitalizacoes():
    from dashboards.hospitalizacoes.main import get_data
    return get_data(request)


@app.route("/dashboards/dispositivos", methods=["POST"])
@token_required(required_permissions=["dashboards", "dashboards-dispositivos", "dashboards-dispositivos:read"])
def dashsdispositivos():
    from dashboards.dispositivos.main import get_data
    return get_data(request)


@app.route("/dashboards/movimentacoes", methods=["POST"])
@token_required(required_permissions=["dashboards", "dashboards-movimentacoes", "dashboards-movimentacoes:read"])
def dashsmovimentacoes():
    from dashboards.movimentacoes.main import get_data
    return get_data(request)


@app.route("/dashboards/infeccoes", methods=["POST"])
@token_required(required_permissions=["dashboards", "dashboards-infeccoes", "dashboards-infeccoes:read"])
def dashsinfeccoes():
    from dashboards.infeccoes.main import get_data
    return get_data(request)


@app.route("/paineis/gestaorisco", methods=["POST"])
@token_required(required_permissions=["paineis", "paineis-gestaorisco", "paineis-gestaorisco:read"])
def paineisgestaorisco():
    from paineis.gestao_risco.main import get_data
    return get_data(request)


@app.route("/orcamentos", methods=["POST"])
@token_required(required_permissions=["orcamentos", "orcamentos:read"])
def orca():
    from orcamentos.main import get_orcamentos
    return get_orcamentos()


@app.route("/produtosconvenio", methods=["POST"])
@token_required(required_permissions=["produtosconvenio", "produtosconvenio:read"])
def prod():
    from mapa.produto_convenio.main import get_produtos_convenio
    return get_produtos_convenio(request)


@app.route("/detalhesmod", methods=["POST"])
@token_required(required_permissions=["detalhesmod", "detalhesmod:read"])
def detalhes_mod():
    from orcamentos.main import get_detalhes_mod
    return get_detalhes_mod(request)


@app.route("/datasets/atendimento_completo", methods=["POST"])
@token_required(required_permissions=["detalhesmod", "detalhesmod:read"])
def datasets_atendimento_completo():
    from datasets.atendimentos_completo.main import get_data
    return get_data(request)


if __name__ == "__main__":
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    context = ('ganep_lar/services/cert/fullchain.pem', 'ganep_lar/services/cert/privkey.pem')
    app.run(host='192.168.77.212', port=5000, ssl_context=context)







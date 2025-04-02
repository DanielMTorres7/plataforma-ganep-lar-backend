from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId

from services.mongo.main import db

users_collection = db['users']

# Definição de roles (mesma estrutura)
roles = {
    'admin': [
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
        'detalhesmod:read',
        'datasets-atendimento_completo',
        'datasets-atendimento_completo:read',
    ],
    'moderator': []  # Moderador herda as permissões do admin
}
roles['moderator'].extend(roles['admin'])

# Decorator para verificar permissões (adaptado para MongoDB)
def token_required(required_permissions=None, required_role=None):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated(*args, **kwargs):
            current_user_id = get_jwt_identity()
            
            # Busca o usuário no MongoDB
            user = users_collection.find_one({'_id': ObjectId(current_user_id)})
            
            if not user:
                return jsonify({'message': 'Usuário não encontrado!'}), 403

            # Verifica se o usuário tem a role necessária
            if user['role'] not in roles:
                return jsonify({'message': 'Unauthorized: Role required!'}), 403

            if required_role and user['role'] != required_role:
                return jsonify({'message': 'Unauthorized: Role required!'}), 403

            # Verifica as permissões
            if required_permissions:
                user_permissions = roles[user['role']]
                for permission in required_permissions:
                    if permission not in user_permissions:
                        return jsonify({'message': 'Unauthorized: Permission required!'}), 403

            return f(*args, **kwargs)
        return decorated
    return decorator

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nome = data.get('nome')
    sobrenome = data.get('sobrenome')
    usuario = data.get('usuario')
    email = data.get('email')
    senha = data.get('senha')
    role = data.get('role', 'user')
    permissions = data.get('permissions', '')

    # Verifica se o usuário já existe
    if users_collection.find_one({'$or': [{'usuario': usuario}, {'email': email}]}):
        return jsonify({"msg": "Usuário já existe"}), 400

    # Cria o novo usuário
    new_user = {
        'nome': nome,
        'sobrenome': sobrenome,
        'usuario': usuario,
        'email': email,
        'role': role,
        'permissions': permissions,
        'password_hash': generate_password_hash(senha)
    }

    # Insere no MongoDB
    result = users_collection.insert_one(new_user)
    
    return jsonify({
        "msg": "Usuário criado com sucesso",
        "id": str(result.inserted_id)
    }), 201

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400

    # Busca o usuário no MongoDB
    user = users_collection.find_one({'email': email})

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Email ou senha inválidos'}), 401

    # Cria o token JWT usando o ObjectId como identity
    access_token = create_access_token(
        identity=str(user['_id']),
        additional_claims={
            'role': user['role'],
            'permissions': user.get('permissions', '')
        }
    )

    return jsonify({
        'token': access_token,
        'user': {
            'id': str(user['_id']),
            'email': user['email'],
            'role': user['role']
        }
    }), 200
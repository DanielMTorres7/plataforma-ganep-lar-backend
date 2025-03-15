from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from services.data_base.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity


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

# Decorator para verificar permissões
def token_required(required_permissions=None, required_role=None):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated(*args, **kwargs):
            current_user = get_jwt_identity()
            user: User = User.query.get(current_user)

            if not user:
                return jsonify({'message': 'Usuário não encontrado!'}), 403

            # Verifica se o usuário tem a role necessária
            if user.role not in roles:
                return jsonify({'message': 'Unauthorized: Role required!'}), 403

            if required_role and user.role != required_role:
                return jsonify({'message': 'Unauthorized: Role required!'}), 403

            # Verifica as permissões
            if required_permissions:
                user_permissions = roles[user.role]
                for permission in required_permissions:
                    if permission not in user_permissions:
                        return jsonify({'message': 'Unauthorized: Permission required!'}), 403

            return f(*args, **kwargs)
        return decorated
    return decorator



auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@token_required(required_role='admin')
def register():
    data = request.get_json()
    nome = data.get('nome')
    sobrenome = data.get('sobrenome')
    usuario = data.get('usuario')
    email = data.get('email')
    senha = data.get('senha')
    role = data.get('role', 'user')
    permissions = data.get('permissions', '')

    if User.query.filter_by(usuario=usuario).first():
        return jsonify({"msg": "Usuário já existe"}), 400

    new_user = User(
        nome=nome,
        sobrenome=sobrenome,
        usuario=usuario,
        email=email,
        role=role,
        permissions=permissions
    )
    new_user.set_password(senha)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Usuário criado com sucesso"}), 201

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400

    # Verifica o usuário no banco de dados
    user: User = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Email ou senha inválidos'}), 401

    # Cria o token JWT
    access_token = create_access_token(
        identity=str(user.id), 
        
        additional_claims={
            'role': user.role,
            'permissions': ''
        }
    )

    return jsonify({'token': access_token}), 200
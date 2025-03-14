from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from services.data_base.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

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
    access_token = create_access_token(identity=str(user.id), additional_claims={
        'role': user.role,
        'permissions': ''
    })

    return jsonify({'token': access_token}), 200
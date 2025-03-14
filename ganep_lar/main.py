from config import Config
import locale
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from services.data_base.models import db, User
from routes import auth_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Inicializa o banco de dados e o JWT
db.init_app(app)
jwt = JWTManager(app)

# Registra o blueprint de autenticação
app.register_blueprint(auth_bp)

# Cria as tabelas do banco de dados
with app.app_context():
    db.create_all()

# Definição de roles e permissões
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
def token_required(required_permissions=None):
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

            # Verifica as permissões
            if required_permissions:
                user_permissions = roles[user.role]
                for permission in required_permissions:
                    if permission not in user_permissions:
                        return jsonify({'message': 'Unauthorized: Permission required!'}), 403

            return f(*args, **kwargs)
        return decorated
    return decorator

# Rotas protegidas
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
@token_required(required_permissions=["datasets-atendimento_completo", "datasets-atendimento_completo:read"])
def datasets_atendimento_completo():
    from datasets.atendimentos_completo.main import get_data
    return get_data(request)

# Inicialização do servidor
if __name__ == "__main__":
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    context = ('ganep_lar/services/cert/fullchain.pem', 'ganep_lar/services/cert/privkey.pem')
    app.run(host='192.168.77.212', port=5000, ssl_context=context)
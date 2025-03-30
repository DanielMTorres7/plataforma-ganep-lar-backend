from config import Config
import locale
from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes import auth_bp, token_required

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={
    r"/orcamentos": {
        "origins": "https://gestaoativa.dstorres.com.br",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Inicializa o banco de dados e o JWT
jwt = JWTManager(app)

# Registra o blueprint de autenticação
app.register_blueprint(auth_bp)

# Definição de roles e permissões

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

@app.route("/paineis/bolinha", methods=["POST"])
@token_required(required_permissions=["paineis", "paineis-gestaorisco", "paineis-gestaorisco:read"])
def paineis_bolinha():
    from paineis.bolinha.main import get_data
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

@app.route("/prontuario", methods=["POST"])
@token_required()
def pront():
    from aj import get_df
    return get_df(request.json.get("prontuario"))

@app.route('/download', methods=["POST"])
@token_required()
def download_xlsx():
    from dashboards.lpp.main import download_xlsx
    return download_xlsx(request)

# Inicialização do servidor
if __name__ == "__main__":
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    context = ('ganep_lar/services/cert/fullchain.pem', 'ganep_lar/services/cert/privkey.pem')
    app.run(host='192.168.77.212', port=5000, ssl_context=context)
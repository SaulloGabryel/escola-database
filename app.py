from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from routes.alunos import alunos_bp
from routes.cursos import cursos_bp
from routes.matriculas import matriculas_bp
from config.database import init_db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Inicializa o banco de dados
init_db()

# Registra os blueprints (rotas)
app.register_blueprint(alunos_bp, url_prefix='/alunos')
app.register_blueprint(cursos_bp, url_prefix='/cursos')
app.register_blueprint(matriculas_bp, url_prefix='/matriculas')

# Swagger UI
SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "API Escola"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def index():
    return {
        "message": "API Escola - Online",
        "docs": "/docs",
        "endpoints": {
            "alunos": "/alunos",
            "cursos": "/cursos",
            "matriculas": "/matriculas"
        }
    }

if __name__ == '__main__':
    app.run(debug=True)

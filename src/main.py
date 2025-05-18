# /home/ubuntu/etiqueta_site/src/main.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, render_template, send_from_directory, session, redirect, url_for
from src.extensions import db
from src.routes.etiqueta_routes import etiqueta_bp
from src.routes.auth_routes import auth_bp
from src.routes.admin_routes import admin_bp
from src.models.user import Usuario
from src.models.etiqueta import Etiqueta
from src.models.predefinicao import Predefinicao
import os

app = Flask(__name__, static_folder='static')

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///etiquetas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chave_secreta_para_sessoes'  # Importante para sessões

# Inicializar extensões
db.init_app(app)

# Registrar blueprints
app.register_blueprint(etiqueta_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
# Rota principal para servir o frontend
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Rota para a área administrativa
@app.route('/admin')
def admin():
    return send_from_directory(app.static_folder, 'admin.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

# Função para criar tabelas e usuários iniciais
def create_tables_and_admin():
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        
        # Verificar se já existem usuários
        if Usuario.query.count() == 0:
            # Criar usuário admin
            admin = Usuario(
                username='admin',
                password='admin123',
                nome_completo='Administrador',
                email='admin@example.com'
            )
            
            # Criar usuário comum
            usuario = Usuario(
                username='usuario',
                password='senha123',
                nome_completo='Usuário Teste',
                email='usuario@example.com'
            )
            
            # Adicionar ao banco de dados
            db.session.add(admin)
            db.session.add(usuario)
            db.session.commit()
            
            print("Usuários iniciais criados: admin/admin123 e usuario/senha123")

# Inicializar o banco de dados e criar usuários iniciais
with app.app_context():
    create_tables_and_admin()

# Iniciar o servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# /home/ubuntu/etiqueta_site/src/models/user.py
from src.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    nome_completo = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)  # Novo campo para identificar administradores
    assinatura_id = db.Column(db.Integer, db.ForeignKey('assinaturas.id'), nullable=True)  # Relacionamento com assinatura
    
    # Relacionamentos
    etiquetas = db.relationship('Etiqueta', backref='usuario', lazy=True)
    predefinicoes = db.relationship('Predefinicao', backref='usuario', lazy=True)
    
    def __init__(self, username, password, nome_completo=None, email=None, is_admin=False, assinatura_id=None):
        self.username = username
        self.set_password(password)
        self.nome_completo = nome_completo
        self.email = email
        self.is_admin = is_admin
        self.assinatura_id = assinatura_id
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Usuario {self.username}>'

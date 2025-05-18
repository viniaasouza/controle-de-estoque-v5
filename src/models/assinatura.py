# /home/ubuntu/etiqueta_site/src/models/assinatura.py
from src.extensions import db
from datetime import datetime

class Assinatura(db.Model):
    __tablename__ = 'assinaturas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_empresa = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    ativa = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    usuarios = db.relationship('Usuario', backref='assinatura', lazy=True)
    
    def __repr__(self):
        return f'<Assinatura {self.nome_empresa} - {self.cnpj}>'

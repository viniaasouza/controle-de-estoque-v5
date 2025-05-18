# /home/ubuntu/etiqueta_site/src/models/predefinicao.py
from src.extensions import db
from datetime import datetime

class Predefinicao(db.Model):
    __tablename__ = 'predefinicoes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_predefinicao = db.Column(db.String(100), nullable=False)
    nome_produto = db.Column(db.String(100), nullable=False)
    tamanho_etiqueta = db.Column(db.String(20), nullable=False, default='80x50')
    classificacao = db.Column(db.String(20), nullable=False, default='Resfriado')  # Novo campo: Seco, Resfriado ou Congelado
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    def __repr__(self):
        return f'<Predefinicao {self.nome_predefinicao}>'

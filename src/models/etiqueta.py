# /home/ubuntu/etiqueta_site/src/models/etiqueta.py
from src.extensions import db
from datetime import datetime

class Etiqueta(db.Model):
    __tablename__ = 'etiquetas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.String(100), nullable=False)
    data_fabricacao = db.Column(db.String(10), nullable=False)  # Formato YYYY-MM-DD
    data_validade = db.Column(db.String(10), nullable=False)    # Formato YYYY-MM-DD
    lote = db.Column(db.String(20), nullable=False)
    tamanho_etiqueta = db.Column(db.String(20), nullable=False, default='80x50')
    classificacao = db.Column(db.String(20), nullable=False, default='Resfriado')  # Novo campo: Seco, Resfriado ou Congelado
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    def __repr__(self):
        return f'<Etiqueta {self.nome_produto} - Lote {self.lote}>'

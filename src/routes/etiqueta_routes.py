# /home/ubuntu/etiqueta_site/src/routes/etiqueta_routes.py
from flask import Blueprint, request, jsonify, send_file, session, redirect, url_for
from src.models.etiqueta import Etiqueta
from src.models.predefinicao import Predefinicao
from src.extensions import db
from fpdf import FPDF
import os
import datetime
import re
from functools import wraps

etiqueta_bp = Blueprint('etiqueta_bp', __name__)

# Decorator para verificar autenticação
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Autenticação necessária"}), 401
        return f(*args, **kwargs)
    return decorated_function

# Função para validar e sanitizar datas
def validate_and_sanitize_date(date_str):
    """
    Valida e sanitiza uma string de data para o formato YYYY-MM-DD.
    Retorna a data sanitizada ou None se inválida.
    """
    if not date_str:
        return None
    
    # Se já estiver no formato YYYY-MM-DD, verifica se é válida
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        try:
            year, month, day = map(int, date_str.split('-'))
            datetime.date(year, month, day)  # Verifica se é uma data válida
            return date_str
        except ValueError:
            return None
    
    # Tenta converter de DD/MM/YYYY para YYYY-MM-DD
    if '/' in date_str:
        parts = date_str.split('/')
        if len(parts) == 3:
            try:
                # Assume DD/MM/YYYY
                day, month, year = map(int, parts)
                # Verifica se o ano tem 2 dígitos
                if year < 100:
                    year = 2000 + year if year < 70 else 1900 + year
                
                # Verifica se é uma data válida
                datetime.date(year, month, day)
                return f"{year:04d}-{month:02d}-{day:02d}"
            except ValueError:
                pass
            
            try:
                # Tenta MM/DD/YYYY (formato americano)
                month, day, year = map(int, parts)
                # Verifica se o ano tem 2 dígitos
                if year < 100:
                    year = 2000 + year if year < 70 else 1900 + year
                
                # Verifica se é uma data válida
                datetime.date(year, month, day)
                return f"{year:04d}-{month:02d}-{day:02d}"
            except ValueError:
                pass
    
    # Tenta converter de DD-MM-YYYY para YYYY-MM-DD
    if '-' in date_str and not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        parts = date_str.split('-')
        if len(parts) == 3:
            try:
                # Assume DD-MM-YYYY
                day, month, year = map(int, parts)
                # Verifica se o ano tem 2 dígitos
                if year < 100:
                    year = 2000 + year if year < 70 else 1900 + year
                
                # Verifica se é uma data válida
                datetime.date(year, month, day)
                return f"{year:04d}-{month:02d}-{day:02d}"
            except ValueError:
                pass
    
    # Tenta converter usando datetime
    try:
        date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        pass
    
    try:
        date_obj = datetime.datetime.strptime(date_str, "%d-%m-%Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        pass
    
    # Se chegou aqui, não conseguiu converter
    return None

@etiqueta_bp.route('/etiquetas', methods=['POST'])
@login_required
def criar_etiqueta():
    try:
        data = request.get_json()
        
        # Validação básica
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        nome_produto = data.get('nome_produto')
        data_fabricacao_raw = data.get('data_fabricacao')
        data_validade_raw = data.get('data_validade')
        tamanho_etiqueta = data.get('tamanho_etiqueta', '80x50')  # Padrão se não fornecido
        
        if not nome_produto:
            return jsonify({"error": "Nome do produto é obrigatório"}), 400
        
        # Validação e sanitização das datas
        data_fabricacao = validate_and_sanitize_date(data_fabricacao_raw)
        if not data_fabricacao:
            return jsonify({"error": f"Data de fabricação inválida: {data_fabricacao_raw}. Use o formato YYYY-MM-DD."}), 400
        
        data_validade = validate_and_sanitize_date(data_validade_raw)
        if not data_validade:
            return jsonify({"error": f"Data de validade inválida: {data_validade_raw}. Use o formato YYYY-MM-DD."}), 400
        
        # Geração automática de lote (YYYYMMDD-HHMMSS)
        now = datetime.datetime.now()
        lote = now.strftime("%Y%m%d-%H%M%S")
        
        # Obter classificação do item
        classificacao = data.get('classificacao', 'Resfriado')  # Padrão se não fornecido
        
        # Criar etiqueta no banco de dados
        nova_etiqueta = Etiqueta(
            nome_produto=nome_produto,
            data_fabricacao=data_fabricacao,
            data_validade=data_validade,
            lote=lote,
            tamanho_etiqueta=tamanho_etiqueta,
            classificacao=classificacao,
            usuario_id=session.get('user_id')
        )
        
        db.session.add(nova_etiqueta)
        db.session.commit()
        
        # Gerar PDF
        pdf = gerar_pdf_etiqueta(nova_etiqueta)
        
        # Salvar PDF temporariamente
        temp_pdf_path = f"/tmp/etiqueta_{nova_etiqueta.id}.pdf"
        pdf.output(temp_pdf_path)
        
        # Enviar PDF como resposta
        return send_file(
            temp_pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"etiqueta_{nome_produto.replace(' ', '_')}_{lote}.pdf"
        )
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def gerar_pdf_etiqueta(etiqueta):
    # Definir tamanho do PDF com base no tamanho da etiqueta
    tamanho = etiqueta.tamanho_etiqueta
    if tamanho == '50x30':
        width, height = 50, 30
    elif tamanho == '100x50':
        width, height = 100, 50
    else:  # Padrão 80x50
        width, height = 80, 50
    
    # Criar PDF
    pdf = FPDF(orientation='P', unit='mm', format=(width, height))
    pdf.add_page()
    
    # Configurar fonte
    pdf.add_font("NotoSans", fname="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", uni=True)
    pdf.set_font("NotoSans", size=10)
    
    # Margens
    margin = 2
    usable_width = width - 2 * margin
    
    # Adicionar logo no canto superior esquerdo
    logo_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'img', 'logo.png')
    if os.path.exists(logo_path):
        # Calcular tamanho proporcional da logo
        logo_width = usable_width * 0.25
        logo_height = logo_width * 0.3  # Proporção aproximada da logo
        # Posicionar logo no canto superior esquerdo
        pdf.image(logo_path, x=margin, y=margin, w=logo_width)
        
        # Ajustar posição inicial do título para não sobrepor a logo
        title_x = margin + logo_width + 2
        title_width = usable_width - logo_width - 2
    else:
        # Se a logo não existir, usar toda a largura para o título
        title_x = margin
        title_width = usable_width
    
    # Título (nome do produto)
    pdf.set_xy(title_x, margin)
    pdf.set_font_size(12)
    pdf.cell(title_width, 6, etiqueta.nome_produto, 0, 1, 'C')
    
    # Classificação do item (Seco, Resfriado, Congelado)
    y_pos = margin + 8
    pdf.set_xy(margin, y_pos)
    pdf.set_font_size(10)
    pdf.set_font("NotoSans", 'B', 10)
    pdf.cell(usable_width, 5, etiqueta.classificacao.upper(), 0, 1, 'L')
    
    # Linha separadora
    y_pos += 6
    pdf.set_draw_color(0, 0, 0)  # Preto
    pdf.line(margin, y_pos, width - margin, y_pos)
    
    # Informações
    pdf.set_font("NotoSans", '', 8)
    
    # Formatação das datas para exibição
    data_fab = datetime.datetime.strptime(etiqueta.data_fabricacao, '%Y-%m-%d').strftime('%d/%m/%Y')
    data_val = datetime.datetime.strptime(etiqueta.data_validade, '%Y-%m-%d').strftime('%d/%m/%Y')
    
    y_pos += 4
    pdf.set_xy(margin, y_pos)
    pdf.set_font("NotoSans", 'B', 8)
    pdf.cell(usable_width/3, 4, "MANIPULAÇÃO:", 0, 0, 'L')
    pdf.set_font("NotoSans", '', 8)
    pdf.cell(usable_width*2/3, 4, f"{data_fab}", 0, 1, 'R')
    
    y_pos += 4
    pdf.set_xy(margin, y_pos)
    pdf.set_font("NotoSans", 'B', 8)
    pdf.cell(usable_width/3, 4, "VALIDADE:", 0, 0, 'L')
    pdf.set_font("NotoSans", '', 8)
    pdf.cell(usable_width*2/3, 4, f"{data_val}", 0, 1, 'R')
    
    # Linha separadora
    y_pos += 5
    pdf.line(margin, y_pos, width - margin, y_pos)
    
    # Lote
    y_pos += 4
    pdf.set_xy(margin, y_pos)
    pdf.set_font("NotoSans", 'B', 8)
    pdf.cell(usable_width/3, 4, "LOTE:", 0, 0, 'L')
    pdf.set_font("NotoSans", '', 8)
    pdf.cell(usable_width*2/3, 4, f"{etiqueta.lote}", 0, 1, 'L')
    
    return pdf

@etiqueta_bp.route('/predefinicoes', methods=['GET'])
@login_required
def listar_predefinicoes():
    try:
        predefinicoes = Predefinicao.query.filter_by(usuario_id=session.get('user_id')).all()
        return jsonify([{
            'id': p.id,
            'nome_predefinicao': p.nome_predefinicao,
            'nome_produto': p.nome_produto,
            'tamanho_etiqueta': p.tamanho_etiqueta
        } for p in predefinicoes])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@etiqueta_bp.route('/predefinicoes', methods=['POST'])
@login_required
def criar_predefinicao():
    try:
        data = request.get_json()
        
        # Validação básica
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        nome_predefinicao = data.get('nome_predefinicao')
        nome_produto = data.get('nome_produto')
        tamanho_etiqueta = data.get('tamanho_etiqueta', '80x50')  # Padrão se não fornecido
        
        if not nome_predefinicao or not nome_produto:
            return jsonify({"error": "Nome da pré-definição e nome do produto são obrigatórios"}), 400
        
        # Verificar se já existe uma pré-definição com o mesmo nome para este usuário
        existente = Predefinicao.query.filter_by(
            nome_predefinicao=nome_predefinicao,
            usuario_id=session.get('user_id')
        ).first()
        
        if existente:
            return jsonify({"error": "Já existe uma pré-definição com este nome"}), 400
        
        # Criar pré-definição
        nova_predefinicao = Predefinicao(
            nome_predefinicao=nome_predefinicao,
            nome_produto=nome_produto,
            tamanho_etiqueta=tamanho_etiqueta,
            usuario_id=session.get('user_id')
        )
        
        db.session.add(nova_predefinicao)
        db.session.commit()
        
        return jsonify({
            "message": "Pré-definição criada com sucesso",
            "id": nova_predefinicao.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@etiqueta_bp.route('/predefinicoes/<int:id>', methods=['PUT'])
@login_required
def atualizar_predefinicao(id):
    try:
        predefinicao = Predefinicao.query.filter_by(id=id, usuario_id=session.get('user_id')).first()
        
        if not predefinicao:
            return jsonify({"error": "Pré-definição não encontrada ou sem permissão"}), 404
        
        data = request.get_json()
        
        # Validação básica
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        nome_predefinicao = data.get('nome_predefinicao')
        nome_produto = data.get('nome_produto')
        tamanho_etiqueta = data.get('tamanho_etiqueta')
        
        if nome_predefinicao:
            # Verificar se já existe outra pré-definição com o mesmo nome para este usuário
            existente = Predefinicao.query.filter_by(
                nome_predefinicao=nome_predefinicao,
                usuario_id=session.get('user_id')
            ).first()
            
            if existente and existente.id != id:
                return jsonify({"error": "Já existe outra pré-definição com este nome"}), 400
            
            predefinicao.nome_predefinicao = nome_predefinicao
        
        if nome_produto:
            predefinicao.nome_produto = nome_produto
        
        if tamanho_etiqueta:
            predefinicao.tamanho_etiqueta = tamanho_etiqueta
        
        db.session.commit()
        
        return jsonify({
            "message": "Pré-definição atualizada com sucesso",
            "id": predefinicao.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@etiqueta_bp.route('/predefinicoes/<int:id>', methods=['DELETE'])
@login_required
def excluir_predefinicao(id):
    try:
        predefinicao = Predefinicao.query.filter_by(id=id, usuario_id=session.get('user_id')).first()
        
        if not predefinicao:
            return jsonify({"error": "Pré-definição não encontrada ou sem permissão"}), 404
        
        db.session.delete(predefinicao)
        db.session.commit()
        
        return jsonify({
            "message": "Pré-definição excluída com sucesso"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

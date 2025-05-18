# /home/ubuntu/etiqueta_site/src/routes/admin_routes.py
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from src.models.assinatura import Assinatura
from src.models.user import Usuario
from src.extensions import db
from functools import wraps
import datetime

admin_bp = Blueprint('admin_bp', __name__)

# Decorator para verificar se o usuário é administrador
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Autenticação necessária"}), 401
        
        # Verificar se o usuário é administrador
        user = Usuario.query.get(session['user_id'])
        if not user or not user.is_admin:
            return jsonify({"error": "Acesso restrito a administradores"}), 403
            
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/assinaturas', methods=['GET'])
@admin_required
def listar_assinaturas():
    try:
        assinaturas = Assinatura.query.all()
        return jsonify([{
            'id': a.id,
            'nome_empresa': a.nome_empresa,
            'cnpj': a.cnpj,
            'email': a.email,
            'telefone': a.telefone,
            'data_inicio': a.data_inicio.strftime('%Y-%m-%d'),
            'data_fim': a.data_fim.strftime('%Y-%m-%d'),
            'ativa': a.ativa,
            'data_criacao': a.data_criacao.strftime('%Y-%m-%d %H:%M:%S')
        } for a in assinaturas])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/assinaturas/<int:id>', methods=['GET'])
@admin_required
def obter_assinatura(id):
    try:
        assinatura = Assinatura.query.get(id)
        if not assinatura:
            return jsonify({"error": "Assinatura não encontrada"}), 404
            
        # Obter usuários associados a esta assinatura
        usuarios = Usuario.query.filter_by(assinatura_id=id).all()
        
        return jsonify({
            'id': assinatura.id,
            'nome_empresa': assinatura.nome_empresa,
            'cnpj': assinatura.cnpj,
            'email': assinatura.email,
            'telefone': assinatura.telefone,
            'data_inicio': assinatura.data_inicio.strftime('%Y-%m-%d'),
            'data_fim': assinatura.data_fim.strftime('%Y-%m-%d'),
            'ativa': assinatura.ativa,
            'data_criacao': assinatura.data_criacao.strftime('%Y-%m-%d %H:%M:%S'),
            'usuarios': [{
                'id': u.id,
                'username': u.username,
                'nome_completo': u.nome_completo,
                'email': u.email,
                'ativo': u.ativo
            } for u in usuarios]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/assinaturas', methods=['POST'])
@admin_required
def criar_assinatura():
    try:
        data = request.get_json()
        
        # Validação básica
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        nome_empresa = data.get('nome_empresa')
        cnpj = data.get('cnpj')
        email = data.get('email')
        telefone = data.get('telefone')
        data_inicio_str = data.get('data_inicio')
        data_fim_str = data.get('data_fim')
        
        if not nome_empresa or not cnpj or not email or not telefone or not data_inicio_str or not data_fim_str:
            return jsonify({"error": "Todos os campos são obrigatórios"}), 400
        
        # Verificar se já existe uma assinatura com o mesmo CNPJ
        existente = Assinatura.query.filter_by(cnpj=cnpj).first()
        if existente:
            return jsonify({"error": "Já existe uma assinatura com este CNPJ"}), 400
        
        # Converter strings de data para objetos date
        try:
            data_inicio = datetime.datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
            data_fim = datetime.datetime.strptime(data_fim_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD"}), 400
        
        # Verificar se a data de fim é posterior à data de início
        if data_fim <= data_inicio:
            return jsonify({"error": "A data de fim deve ser posterior à data de início"}), 400
        
        # Criar assinatura
        nova_assinatura = Assinatura(
            nome_empresa=nome_empresa,
            cnpj=cnpj,
            email=email,
            telefone=telefone,
            data_inicio=data_inicio,
            data_fim=data_fim,
            ativa=True
        )
        
        db.session.add(nova_assinatura)
        db.session.commit()
        
        return jsonify({
            "message": "Assinatura criada com sucesso",
            "id": nova_assinatura.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/assinaturas/<int:id>', methods=['PUT'])
@admin_required
def atualizar_assinatura(id):
    try:
        assinatura = Assinatura.query.get(id)
        if not assinatura:
            return jsonify({"error": "Assinatura não encontrada"}), 404
        
        data = request.get_json()
        
        # Validação básica
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        # Atualizar campos
        if 'nome_empresa' in data:
            assinatura.nome_empresa = data['nome_empresa']
        
        if 'email' in data:
            assinatura.email = data['email']
        
        if 'telefone' in data:
            assinatura.telefone = data['telefone']
        
        if 'data_inicio' in data:
            try:
                assinatura.data_inicio = datetime.datetime.strptime(data['data_inicio'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Formato de data de início inválido. Use YYYY-MM-DD"}), 400
        
        if 'data_fim' in data:
            try:
                assinatura.data_fim = datetime.datetime.strptime(data['data_fim'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Formato de data de fim inválido. Use YYYY-MM-DD"}), 400
        
        # Verificar se a data de fim é posterior à data de início
        if assinatura.data_fim <= assinatura.data_inicio:
            return jsonify({"error": "A data de fim deve ser posterior à data de início"}), 400
        
        if 'ativa' in data:
            assinatura.ativa = bool(data['ativa'])
        
        # Não permitir alterar o CNPJ, pois é um identificador único
        
        db.session.commit()
        
        return jsonify({
            "message": "Assinatura atualizada com sucesso",
            "id": assinatura.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/assinaturas/<int:id>', methods=['DELETE'])
@admin_required
def excluir_assinatura(id):
    try:
        assinatura = Assinatura.query.get(id)
        if not assinatura:
            return jsonify({"error": "Assinatura não encontrada"}), 404
        
        # Verificar se existem usuários associados a esta assinatura
        usuarios = Usuario.query.filter_by(assinatura_id=id).all()
        if usuarios:
            return jsonify({"error": "Não é possível excluir uma assinatura com usuários associados"}), 400
        
        db.session.delete(assinatura)
        db.session.commit()
        
        return jsonify({
            "message": "Assinatura excluída com sucesso"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/assinaturas/<int:id>/ativar', methods=['PUT'])
@admin_required
def ativar_assinatura(id):
    try:
        assinatura = Assinatura.query.get(id)
        if not assinatura:
            return jsonify({"error": "Assinatura não encontrada"}), 404
        
        assinatura.ativa = True
        db.session.commit()
        
        return jsonify({
            "message": "Assinatura ativada com sucesso",
            "id": assinatura.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/assinaturas/<int:id>/desativar', methods=['PUT'])
@admin_required
def desativar_assinatura(id):
    try:
        assinatura = Assinatura.query.get(id)
        if not assinatura:
            return jsonify({"error": "Assinatura não encontrada"}), 404
        
        assinatura.ativa = False
        db.session.commit()
        
        return jsonify({
            "message": "Assinatura desativada com sucesso",
            "id": assinatura.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/usuarios', methods=['GET'])
@admin_required
def listar_usuarios():
    try:
        usuarios = Usuario.query.all()
        return jsonify([{
            'id': u.id,
            'username': u.username,
            'nome_completo': u.nome_completo,
            'email': u.email,
            'ativo': u.ativo,
            'is_admin': u.is_admin,
            'assinatura_id': u.assinatura_id
        } for u in usuarios])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/usuarios/<int:id>', methods=['PUT'])
@admin_required
def atualizar_usuario(id):
    try:
        usuario = Usuario.query.get(id)
        if not usuario:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        data = request.get_json()
        
        # Validação básica
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        # Atualizar campos
        if 'nome_completo' in data:
            usuario.nome_completo = data['nome_completo']
        
        if 'email' in data:
            # Verificar se o email já está em uso por outro usuário
            existente = Usuario.query.filter(Usuario.email == data['email'], Usuario.id != id).first()
            if existente:
                return jsonify({"error": "Este email já está em uso por outro usuário"}), 400
            usuario.email = data['email']
        
        if 'ativo' in data:
            usuario.ativo = bool(data['ativo'])
        
        if 'is_admin' in data:
            usuario.is_admin = bool(data['is_admin'])
        
        if 'assinatura_id' in data:
            # Verificar se a assinatura existe
            if data['assinatura_id'] is not None:
                assinatura = Assinatura.query.get(data['assinatura_id'])
                if not assinatura:
                    return jsonify({"error": "Assinatura não encontrada"}), 400
            usuario.assinatura_id = data['assinatura_id']
        
        if 'password' in data and data['password']:
            usuario.set_password(data['password'])
        
        db.session.commit()
        
        return jsonify({
            "message": "Usuário atualizado com sucesso",
            "id": usuario.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/usuarios', methods=['POST'])
@admin_required
def criar_usuario():
    try:
        data = request.get_json()
        
        # Validação básica
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        username = data.get('username')
        password = data.get('password')
        nome_completo = data.get('nome_completo')
        email = data.get('email')
        is_admin = data.get('is_admin', False)
        assinatura_id = data.get('assinatura_id')
        
        if not username or not password:
            return jsonify({"error": "Nome de usuário e senha são obrigatórios"}), 400
        
        # Verificar se o nome de usuário já existe
        existente = Usuario.query.filter_by(username=username).first()
        if existente:
            return jsonify({"error": "Este nome de usuário já está em uso"}), 400
        
        # Verificar se o email já existe
        if email:
            existente = Usuario.query.filter_by(email=email).first()
            if existente:
                return jsonify({"error": "Este email já está em uso"}), 400
        
        # Verificar se a assinatura existe
        if assinatura_id is not None:
            assinatura = Assinatura.query.get(assinatura_id)
            if not assinatura:
                return jsonify({"error": "Assinatura não encontrada"}), 400
        
        # Criar usuário
        novo_usuario = Usuario(
            username=username,
            password=password,
            nome_completo=nome_completo,
            email=email,
            is_admin=is_admin,
            assinatura_id=assinatura_id
        )
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        return jsonify({
            "message": "Usuário criado com sucesso",
            "id": novo_usuario.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

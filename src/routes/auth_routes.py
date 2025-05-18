# /home/ubuntu/etiqueta_site/src/routes/auth_routes.py
from flask import Blueprint, request, jsonify, session
from src.models.user import Usuario
from src.extensions import db

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "Nome de usuário e senha são obrigatórios"}), 400
        
        # Buscar usuário pelo nome de usuário
        usuario = Usuario.query.filter_by(username=username).first()
        
        # Verificar se o usuário existe e a senha está correta
        if not usuario or not usuario.check_password(password):
            return jsonify({"error": "Nome de usuário ou senha incorretos"}), 401
        
        # Verificar se o usuário está ativo
        if not usuario.ativo:
            return jsonify({"error": "Conta desativada. Entre em contato com o administrador."}), 403
        
        # Criar sessão para o usuário
        session['user_id'] = usuario.id
        session['username'] = usuario.username
        
        return jsonify({
            "message": "Login realizado com sucesso",
            "user": {
                "id": usuario.id,
                "username": usuario.username,
                "nome_completo": usuario.nome_completo
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Limpar a sessão
    session.clear()
    return jsonify({"message": "Logout realizado com sucesso"})

@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    if 'user_id' in session:
        usuario = Usuario.query.get(session['user_id'])
        if usuario:
            return jsonify({
                "authenticated": True,
                "user": {
                    "id": usuario.id,
                    "username": usuario.username,
                    "nome_completo": usuario.nome_completo
                }
            })
    
    return jsonify({"authenticated": False})

Documentação do Sistema StockEasy - Gerador de Etiquetas para Restaurantes
Visão Geral
O StockEasy é um sistema completo para geração de etiquetas para restaurantes, permitindo o controle de produtos, datas de fabricação e validade, com suporte a classificação de itens (Seco, Resfriado ou Congelado) e gestão de assinaturas.

Melhorias Implementadas na Versão 2
1. Identidade Visual StockEasy
Adicionada a logo StockEasy no canto superior esquerdo das etiquetas
Implementada a identidade visual com cores padronizadas em toda a interface
2. Classificação de Itens
Adicionada barra de opções para classificação dos itens como "Seco", "Resfriado" ou "Congelado"
A classificação é exibida na etiqueta gerada, facilitando a identificação visual
3. Correção de Problemas
Corrigido o erro 500 que ocorria durante a geração de etiquetas
Melhorado o tratamento de formatos de data para aceitar diferentes padrões de entrada
4. Área Administrativa
Implementada área administrativa para gestão de assinaturas
Interface completa para cadastro, edição e exclusão de assinaturas
Proteção de acesso com verificação de permissões administrativas
Estrutura do Sistema
Frontend
Interface principal para geração de etiquetas
Área de login com controle de sessão
Área administrativa para gestão de assinaturas
Visualização e gerenciamento de pré-definições
Backend
API RESTful para comunicação com o frontend
Sistema de autenticação e controle de acesso
Geração de PDFs para impressão de etiquetas
Gestão de assinaturas e usuários
Credenciais de Acesso
Usuário Administrador
Usuário: admin
Senha: admin123
Permissões: Acesso total ao sistema, incluindo área administrativa
Usuário Comum
Usuário: usuario
Senha: senha123
Permissões: Acesso à geração de etiquetas e gerenciamento de pré-definições
Instruções de Uso
Geração de Etiquetas
Faça login no sistema com suas credenciais
Preencha o formulário com o nome do produto
Defina as datas de fabricação e validade
Selecione a classificação do item (Seco, Resfriado ou Congelado)
Escolha o tamanho da etiqueta
Clique em "Gerar e Baixar Etiqueta PDF"
Gerenciamento de Pré-definições
Acesse a seção "Pré-definições de Etiquetas"
Preencha o formulário com o nome da pré-definição e dados do produto
Clique em "Salvar Pré-definição"
Para usar uma pré-definição, clique em "Usar" na lista de pré-definições
Área Administrativa (apenas para administradores)
Acesse a URL "/admin" após fazer login como administrador
Utilize as abas para navegar entre "Assinaturas" e "Usuários"
Para adicionar uma nova assinatura, clique em "Nova Assinatura"
Para gerenciar usuários, utilize a aba "Usuários"
Instruções de Instalação
Descompacte o arquivo etiqueta_site_v4_final.zip
Crie e ative um ambiente virtual Python:
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
Instale as dependências:
pip install -r requirements.txt
Inicie o servidor:
python -m src.main
Acesse o sistema em http://localhost:5000
Requisitos do Sistema
Python 3.8 ou superior
Navegador web moderno (Chrome, Firefox, Edge, Safari)
Conexão com a internet para carregamento de fontes e ícones
Suporte
Para suporte técnico ou dúvidas sobre o sistema, entre em contato com a equipe StockEasy.

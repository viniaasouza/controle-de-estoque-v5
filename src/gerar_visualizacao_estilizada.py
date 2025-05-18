import os
import sys
from fpdf import FPDF
from PIL import Image
import datetime
import qrcode

def gerar_visualizacao_etiqueta_estilizada():
    # Dados de exemplo
    nome_produto = "Frango Assado"
    tipo_produto = "RESFRIADO"
    data_fabricacao = "18/05/2025"
    data_validade = "20/05/2025"
    hora = "05H31"
    lote = "20250518-123456"
    responsavel = "STOCKEASY"
    empresa = "STOCKEASY - SISTEMA DE ETIQUETAS"
    cnpj = "00.000.000/0001-00"
    endereco = "São Paulo, SP"
    codigo = "#SE12345"
    tamanho = "80x50"  # Padrão 80x50mm
    
    # Definir tamanho do PDF com base no tamanho da etiqueta
    if tamanho == '50x30':
        width, height = 50, 30
    elif tamanho == '100x50':
        width, height = 100, 50
    else:  # Padrão 80x50
        width, height = 80, 50
    
    # Criar PDF
    pdf = FPDF(orientation='P', unit='mm', format=(width, height))
    pdf.add_page()
    
    # Configurar fonte - usando Helvetica (Arial) como alternativa segura
    pdf.set_font("Helvetica", size=10)
    
    # Cores
    azul_stockeasy = (61, 141, 174)  # RGB para azul da logo StockEasy
    preto = (0, 0, 0)
    
    # Margens
    margin = 2
    usable_width = width - 2 * margin
    
    # Fundo branco para toda a etiqueta
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(0, 0, width, height, 'F')
    
    # Adicionar logo StockEasy
    logo_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'img', 'logo.png')
    if os.path.exists(logo_path):
        # Calcular tamanho proporcional da logo
        logo_width = usable_width * 0.3
        logo_height = logo_width * 0.3  # Proporção aproximada da logo
        # Posicionar logo no canto superior esquerdo
        pdf.image(logo_path, x=margin, y=margin, w=logo_width)
    
    # Nome do produto em destaque (parte superior)
    pdf.set_xy(margin, margin)
    pdf.set_font("Helvetica", 'B', 12)  # Bold
    pdf.set_text_color(0, 0, 0)  # Preto
    pdf.cell(usable_width, 6, nome_produto, 0, 1, 'C')
    
    # Tipo de produto (ex: RESFRIADO)
    y_pos = margin + 6
    pdf.set_xy(margin, y_pos)
    pdf.set_font("Helvetica", '', 8)
    pdf.cell(usable_width, 4, tipo_produto, 0, 1, 'L')
    
    # Linha separadora
    y_pos += 5
    pdf.set_draw_color(0, 0, 0)  # Preto
    pdf.line(margin, y_pos, width - margin, y_pos)
    
    # Datas de manipulação e validade
    y_pos += 3
    pdf.set_xy(margin, y_pos)
    pdf.set_font("Helvetica", 'B', 7)
    pdf.cell(usable_width/3, 4, "MANIPULAÇÃO:", 0, 0, 'L')
    pdf.set_font("Helvetica", '', 7)
    pdf.cell(usable_width*2/3, 4, f"{data_fabricacao} - {hora}", 0, 1, 'R')  # Usando hífen normal em vez de travessão
    
    y_pos += 4
    pdf.set_xy(margin, y_pos)
    pdf.set_font("Helvetica", 'B', 7)
    pdf.cell(usable_width/3, 4, "VALIDADE:", 0, 0, 'L')
    pdf.set_font("Helvetica", '', 7)
    pdf.cell(usable_width*2/3, 4, f"{data_validade} - {hora}", 0, 1, 'R')  # Usando hífen normal em vez de travessão
    
    # Linha separadora
    y_pos += 5
    pdf.line(margin, y_pos, width - margin, y_pos)
    
    # Informações da empresa
    y_pos += 3
    pdf.set_xy(margin, y_pos)
    pdf.set_font("Helvetica", 'B', 7)
    pdf.cell(usable_width/3, 4, "RESP.:", 0, 0, 'L')
    pdf.set_font("Helvetica", '', 7)
    pdf.cell(usable_width*2/3, 4, responsavel, 0, 1, 'L')
    
    # Gerar QR code
    qr_data = f"PRODUTO:{nome_produto}\nFABRICAÇÃO:{data_fabricacao}\nVALIDADE:{data_validade}\nLOTE:{lote}\nEMPRESA:{empresa}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_path = "/tmp/qrcode_temp.png"
    qr_img.save(qr_path)
    
    # Adicionar QR code no canto direito
    qr_size = 15  # tamanho em mm
    pdf.image(qr_path, x=width-margin-qr_size, y=y_pos, w=qr_size)
    
    # Informações adicionais da empresa (abaixo do RESP)
    y_pos += 4
    pdf.set_xy(margin, y_pos)
    pdf.set_font("Helvetica", '', 5)
    pdf.cell(usable_width-qr_size-2, 3, empresa, 0, 1, 'L')
    
    y_pos += 3
    pdf.set_xy(margin, y_pos)
    pdf.cell(usable_width-qr_size-2, 3, f"CNPJ: {cnpj}", 0, 1, 'L')
    
    y_pos += 3
    pdf.set_xy(margin, y_pos)
    pdf.cell(usable_width-qr_size-2, 3, endereco, 0, 1, 'L')
    
    y_pos += 3
    pdf.set_xy(margin, y_pos)
    pdf.cell(usable_width-qr_size-2, 3, codigo, 0, 1, 'L')
    
    # Salvar PDF temporariamente
    temp_pdf_path = "/tmp/etiqueta_estilizada.pdf"
    pdf.output(temp_pdf_path)
    
    # Converter PDF para PNG usando PIL
    try:
        # Criar diretório para imagens se não existir
        img_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'img')
        os.makedirs(img_dir, exist_ok=True)
        
        # Caminho para a imagem PNG
        png_path = os.path.join(img_dir, 'etiqueta_estilizada.png')
        
        # Usar pdf2image para converter PDF para PNG
        from pdf2image import convert_from_path
        images = convert_from_path(temp_pdf_path, dpi=300)
        if images:
            images[0].save(png_path, 'PNG')
            print(f"Visualização da etiqueta estilizada gerada em: {png_path}")
            return png_path
        else:
            print("Falha ao converter PDF para PNG")
            return None
    except Exception as e:
        print(f"Erro ao converter PDF para PNG: {e}")
        return None

if __name__ == "__main__":
    gerar_visualizacao_etiqueta_estilizada()

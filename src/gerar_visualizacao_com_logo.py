import os
import sys
from fpdf import FPDF
from PIL import Image
import datetime

def gerar_visualizacao_etiqueta():
    # Dados de exemplo
    nome_produto = "Frango Assado"
    data_fabricacao = "18/05/2025"
    data_validade = "20/05/2025"
    lote = "20250518-123456"
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
    
    # Configurar fonte - usando Arial como alternativa segura
    pdf.set_font("Arial", size=10)
    
    # Margens
    margin = 2
    usable_width = width - 2 * margin
    
    # Adicionar logo StockEasy
    logo_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'img', 'logo.png')
    if os.path.exists(logo_path):
        # Calcular tamanho proporcional da logo
        logo_width = usable_width * 0.4
        logo_height = logo_width * 0.3  # Proporção aproximada da logo
        pdf.image(logo_path, x=(width - logo_width) / 2, y=margin, w=logo_width)
        y_pos = margin + logo_height + 2
    else:
        y_pos = margin
    
    # Título (nome do produto)
    pdf.set_xy(margin, y_pos)
    pdf.set_font_size(12)
    pdf.set_text_color(0, 0, 0)  # Preto
    pdf.cell(usable_width, 6, nome_produto, 0, 1, 'C')
    
    # Informações
    pdf.set_font_size(8)
    
    # Formatação das datas para exibição
    y_pos += 8
    pdf.set_xy(margin, y_pos)
    pdf.set_text_color(61, 141, 174)  # Azul StockEasy
    pdf.cell(usable_width/2, 4, f"Fabricação: {data_fabricacao}", 0, 0, 'L')
    pdf.cell(usable_width/2, 4, f"Validade: {data_validade}", 0, 1, 'R')
    
    # Lote
    y_pos += 5
    pdf.set_xy(margin, y_pos)
    pdf.set_text_color(0, 0, 0)  # Preto
    pdf.cell(usable_width, 4, f"Lote: {lote}", 0, 1, 'C')
    
    # Salvar PDF temporariamente
    temp_pdf_path = "/tmp/etiqueta_exemplo.pdf"
    pdf.output(temp_pdf_path)
    
    # Converter PDF para PNG usando PIL
    try:
        # Criar diretório para imagens se não existir
        img_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'img')
        os.makedirs(img_dir, exist_ok=True)
        
        # Caminho para a imagem PNG
        png_path = os.path.join(img_dir, 'etiqueta_exemplo.png')
        
        # Usar pdf2image para converter PDF para PNG
        from pdf2image import convert_from_path
        images = convert_from_path(temp_pdf_path, dpi=300)
        if images:
            images[0].save(png_path, 'PNG')
            print(f"Visualização da etiqueta gerada em: {png_path}")
            return png_path
        else:
            print("Falha ao converter PDF para PNG")
            return None
    except Exception as e:
        print(f"Erro ao converter PDF para PNG: {e}")
        return None

if __name__ == "__main__":
    gerar_visualizacao_etiqueta()

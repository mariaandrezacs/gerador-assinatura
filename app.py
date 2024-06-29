from flask import Flask, request, render_template, send_file
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

def create_email_signature(name, title, department, phone, email, website):
    # Definindo as dimensões da imagem da assinatura
    width, height = 800, 162  # Largura e altura desejadas da assinatura
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    font_size = 18  # Tamanho da fonte
    font_path = "arial.ttf"  # Certifique-se de que o arquivo de fonte está disponível

    # Abrindo a logo
    logo_path = "static/logo.png"  # Certifique-se de que o arquivo da logo está no diretório correto
    try:
        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize((width, height))  # Redimensionando a logo para as novas dimensões da assinatura
    except IOError:
        print("Logo não encontrada. Certifique-se de que o arquivo da logo está no diretório correto.")
        return

    # Criando uma nova imagem com fundo branco
    img = Image.new("RGBA", (width, height), background_color)
    draw = ImageDraw.Draw(img)

    # Combinando a logo com a imagem de fundo
    img.paste(logo, (0, 0), logo)  # Colocando a logo como fundo, preservando a transparência

    # Carregando a fonte com o tamanho especificado
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Fonte não encontrada. Certifique-se de que o arquivo de fonte está no diretório correto.")
        return

    # Definindo as posições dos textos
    width = 20
    x, y = width, width

    # Escrevendo os textos na imagem
    draw.text((x, y), name, fill=text_color, font=font)
    y += font_size + 2
    draw.text((x, y), title, fill=text_color, font=font)
    y += font_size + 5
    draw.text((x, y), department, fill=text_color, font=font)
    y += font_size + 2
    draw.text((x, y), phone, fill=text_color, font=font)
    y += font_size + 2
    draw.text((x, y), email, fill=text_color, font=font)
    y += font_size + 2
    draw.text((x, y), website, fill=text_color, font=font)

    # Salvando a imagem
    img = img.convert("RGB")  # Converte de RGBA para RGB para salvar como PNG
    signature_path = "static/assinatura_email.png"
    img.save(signature_path)
    print("Assinatura de email gerada com sucesso!")
    return signature_path

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/generate_signature', methods=['POST'])
def generate_signature():
    name = request.form['name']
    title = request.form['title']
    department = request.form['department']
    phone = request.form['phone']
    email = request.form['email']
    website = request.form['website']

    signature_path = create_email_signature(name, title, department, phone, email, website)
    return '''
    <h2>Assinatura de email gerada com sucesso!</h2>
    <img src="/static/assinatura_email.png" alt="Assinatura de Email">
    <br><br>
    <a href="/download">Baixar Assinatura</a>
    '''

@app.route('/download')
def download_signature():
    signature_path = "static/assinatura_email.png"
    return send_file(signature_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

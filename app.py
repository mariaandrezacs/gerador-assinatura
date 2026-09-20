import os

from flask import Flask, request, render_template, send_file, url_for
from PIL import Image, ImageDraw, ImageFont, ImageOps
from werkzeug.utils import secure_filename

app = Flask(__name__)

# URL pública da logo usada na assinatura HTML. Para o HTML funcionar no cliente
# de email dos destinatários, hospede a imagem e aponte aqui
# (ex.: "https://seudominio.com/logo-b.png"). Se None, usa a URL local.
PUBLIC_LOGO_URL = None

# Dimensões recomendadas para assinatura de email: 300-400 x 70-100 px
SIGNATURE_WIDTH, SIGNATURE_HEIGHT = 400, 85
SIGNATURE_PATH = "static/assinatura_email.png"


def _text_start_x(logo, margin=8):
    """Detecta até onde vai o conteúdo escuro na esquerda (ex.: símbolo da logo)
    para posicionar o texto depois dele, evitando sobreposição."""
    px = logo.convert("RGB").load()
    w, h = logo.size
    last = 0
    for x in range(w // 3):
        for y in range(h):
            r, g, b = px[x, y]
            if r + g + b < 150:
                last = x
                break
    return last + margin if last else 12


def create_email_signature(name, title, department, phone, email, website, background_path="static/logo-b.png"):
    background_color = (255, 255, 255)
    text_color = (10, 46, 92)  # azul escuro, legível sobre o gradiente claro
    font_path = "arial.ttf"  # Certifique-se de que o arquivo de fonte está disponível

    # Abrindo a imagem de fundo
    logo_path = background_path  # Certifique-se de que o arquivo da logo está no diretório correto
    try:
        logo = Image.open(logo_path).convert("RGBA")
        # Ajusta às dimensões da assinatura mantendo a proporção
        # (redimensiona e corta o excesso no centro, sem distorcer)
        logo = ImageOps.fit(logo, (SIGNATURE_WIDTH, SIGNATURE_HEIGHT), Image.LANCZOS)
    except IOError:
        print("Imagem de fundo não encontrada. Usando fundo branco.")
        logo = Image.new("RGBA", (SIGNATURE_WIDTH, SIGNATURE_HEIGHT), background_color)

    # Criando uma nova imagem com fundo branco
    img = Image.new("RGBA", (SIGNATURE_WIDTH, SIGNATURE_HEIGHT), background_color)
    draw = ImageDraw.Draw(img)

    # Combinando a logo com a imagem de fundo
    img.paste(logo, (0, 0), logo)  # Colocando a logo como fundo, preservando a transparência

    # Carregando as fontes
    try:
        font_name = ImageFont.truetype(font_path, 13)
        font = ImageFont.truetype(font_path, 11)
    except IOError:
        print("Fonte não encontrada. Certifique-se de que o arquivo de fonte está no diretório correto.")
        return

    # Texto começa após o símbolo na borda esquerda da imagem de fundo
    x, y = _text_start_x(logo), 6
    line_height = 13

    draw.text((x, y), name, fill=text_color, font=font_name)
    y += 16

    lines = [
        f"{title} · {department}" if department else title,
        phone,
        email,
        website,
    ]
    for line in filter(None, lines):
        draw.text((x, y), line, fill=text_color, font=font)
        y += line_height

    # Salvando a imagem
    img = img.convert("RGB")  # Converte de RGBA para RGB para salvar como PNG
    img.save(SIGNATURE_PATH)
    print("Assinatura de email gerada com sucesso!")
    return SIGNATURE_PATH


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
    website = request.form['website'].strip()

    # Imagem de fundo enviada pelo usuário (opcional)
    background_file = request.files.get('background')
    background_filename = None
    warning = None
    if background_file and background_file.filename:
        ext = os.path.splitext(secure_filename(background_file.filename))[1].lower()
        if ext in ('.png', '.jpg', '.jpeg'):
            save_path = os.path.join('static', f"fundo_custom{ext}")
            background_file.save(save_path)
            try:
                with Image.open(save_path) as bg:
                    bw, bh = bg.size
            except Exception:
                os.remove(save_path)
                warning = "O arquivo enviado não é uma imagem válida. Foi usado o fundo padrão."
            else:
                background_filename = f"fundo_custom{ext}"
                if bw < 300 or bh < 70:
                    warning = (f"A imagem enviada ({bw}×{bh} px) é menor que o recomendado "
                               f"(300–400 × 70–100 px) e pode ficar com baixa qualidade.")
                elif bw > 800 or bh > 200:
                    warning = (f"A imagem enviada ({bw}×{bh} px) é maior que o recomendado "
                               f"(300–400 × 70–100 px) e será reduzida para 400×85 px.")
                elif abs(bw / bh - SIGNATURE_WIDTH / SIGNATURE_HEIGHT) > 0.5:
                    warning = (f"A proporção da imagem enviada ({bw}×{bh} px) difere da assinatura; "
                               f"as bordas serão cortadas para ajustar a 400×85 px.")

    background_path = os.path.join('static', background_filename) if background_filename else "static/logo-b.png"
    create_email_signature(name, title, department, phone, email, website, background_path)

    logo_url = PUBLIC_LOGO_URL or url_for(
        'static', filename=background_filename or 'logo-b.png', _external=True)
    website_url = ""
    if website:
        website_url = website if website.startswith(("http://", "https://")) else f"https://{website}"

    signature_html = render_template(
        'signature.html',
        name=name,
        title=title,
        department=department,
        phone=phone,
        email=email,
        website=website,
        website_url=website_url,
        logo_url=logo_url,
    )
    return render_template('result.html', signature_html=signature_html, warning=warning)


@app.route('/download')
def download_signature():
    return send_file(SIGNATURE_PATH, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

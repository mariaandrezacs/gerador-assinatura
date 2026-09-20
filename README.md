# Gerador de Assinatura de Email

Aplicação web em Flask para criar assinaturas de email profissionais. Gera uma imagem PNG nas dimensões recomendadas (400 × 85 px) e também uma versão HTML copiável — com texto selecionável e links clicáveis — para colar direto no cliente de email.

## Funcionalidades

- Formulário com nome, cargo, departamento, telefone, email e site
- Upload opcional de imagem de fundo personalizada (`.png`, `.jpg`, `.jpeg`)
- Ajuste automático da imagem sem distorção (redimensiona e corta o excesso)
- Aviso quando a imagem enviada está fora do tamanho recomendado (300–400 × 70–100 px)
- Pré-visualização da assinatura gerada
- Download do PNG
- Versão HTML com botão "Copiar assinatura" (Gmail, Outlook etc.)

## Requisitos

- Python 3.10+
- Dependências em `requirements.txt` (Flask, Pillow)

## Como executar

```bash
# Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Rodar o servidor
python app.py
```

Acesse `http://localhost:5000`, preencha o formulário e clique em **Gerar Assinatura**.

## Configuração

No topo de `app.py`:

| Constante | Descrição |
|---|---|
| `PUBLIC_LOGO_URL` | URL pública da imagem usada na assinatura HTML. Para que a imagem apareça no email dos destinatários, hospede-a e aponte aqui (ex.: `https://seudominio.com/logo-b.png`). Se `None`, usa a URL local. |
| `SIGNATURE_WIDTH` / `SIGNATURE_HEIGHT` | Dimensões da assinatura PNG (padrão: 400 × 85 px). |

## Estrutura

```
app.py                    # Aplicação Flask e geração da assinatura PNG
arial.ttf                 # Fonte usada no texto da assinatura
requirements.txt          # Dependências
static/
  logo.png                # Banner da marca (logo roxa)
  logo-b.png              # Banner da marca (logo branca — padrão)
  logo-.png               # Ícone/favicon
  assinatura_email.png    # Última assinatura gerada
templates/
  form.html               # Formulário de entrada
  result.html             # Resultado: PNG + versão HTML copiável
  signature.html          # Template da assinatura HTML
```

## Observações

- A assinatura gerada fica em `static/assinatura_email.png` e é sobrescrita a cada geração.
- Ao colar a versão HTML no Gmail, a imagem é embutida no momento da cópia; para outros clientes ou envio em massa, configure `PUBLIC_LOGO_URL` com a imagem hospedada.

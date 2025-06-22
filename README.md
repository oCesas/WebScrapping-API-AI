# WebScrapping-API-AI
Este projeto foi desenvolvido como parte de um teste técnico para vaga de estágio na empresa Axur. O desafio consistia em realizar o scraping de uma imagem codificada em base64 a partir de uma página HTML, processar essa imagem com um modelo de IA, e submeter a resposta processada via API.

## ⚙️ Tecnologias Utilizadas

- **Python 3**
- [`requests`](https://pypi.org/project/requests/) – Requisições HTTP
- [`BeautifulSoup`](https://pypi.org/project/beautifulsoup4/) – Web scraping de conteúdo HTML
- [`re`](https://docs.python.org/3/library/re.html) – Expressões regulares para encontrar a imagem
- [`base64`](https://docs.python.org/3/library/base64.html) – Codificação/decodificação da imagem
- [`dotenv`](https://pypi.org/project/python-dotenv/) – Carregamento de variáveis de ambiente (opcional)
- [`pathlib`](https://docs.python.org/3/library/pathlib.html) – Manipulação de arquivos com `Path`

---

## 📌 Funcionalidades

- Realiza scraping de uma imagem em base64 contida em uma página HTML.
- Decodifica a imagem e salva localmente no formato `.jpg`.
- Codifica novamente em base64 para envio via API.
- Envia a imagem com um prompt ao modelo `microsoft-florence-2-large`.
- Recebe a resposta gerada e realiza submissão via outra API.

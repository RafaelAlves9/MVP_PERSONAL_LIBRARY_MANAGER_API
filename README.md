## Gerenciador de Livros Lidos (OpenLibrary)

API Flask que pesquisa livros via OpenLibrary e permite marcar como lidos com observação. Os livros pesquisados são cacheados em SQLite para consulta offline e paginação local.

### Endpoints principais
- `GET /books`: busca paginada na OpenLibrary (query: `page`, `limit` até 50, `author`, `title`, `q`).
- `GET /reads`: lista paginada dos livros marcados como lidos localmente (`page`, `per_page`).
- `POST /reads`: body `{"external_id": "<key da OpenLibrary>", "note": "observação opcional"}` para marcar como lido e salvar nota.
- Swagger: `/swagger`.

### Tecnologias
- Flask 3, Flask-RESTX, Flask-SQLAlchemy, Flask-CORS, Requests
- SQLite (padrão, arquivo `instance/books.db`)
- Gunicorn para produção

### Setup local
1) Criar venv (opcional) e instalar dependências:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Rodar a API:
```bash
python run.py
```
Disponível em `http://localhost:5000/swagger`.

### Docker
```bash
docker build -t books-api .
docker run -p 5000:5000 books-api
# opcional: -e PORT=8000 -e GUNICORN_WORKERS=4 -e GUNICORN_THREADS=4
# opcional: -v $(pwd)/instance:/app/instance para persistir o SQLite
```

### Observações
- Cache local com dados básicos (título, autor, ano, capa) para reduzir dependência da API externa.
- Sem necessidade de chave de API para a OpenLibrary.

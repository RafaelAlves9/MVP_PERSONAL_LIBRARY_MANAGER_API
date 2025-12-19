from flask_restx import Api, fields

swagger = Api(
    version="2.0",
    title="Gerenciador de Livros Lidos",
    description="API para pesquisar livros via OpenLibrary e marcar como lidos com observação.",
    doc="/swagger",
)

book_search_filters_model = swagger.model(
    "BookSearchFilters",
    {
        "page": fields.Integer(description="Página (default 1)"),
        "limit": fields.Integer(description="Itens por página (default 10, máx 50)"),
        "author": fields.String(description="Filtra por autor"),
        "title": fields.String(description="Filtra por título"),
        "q": fields.String(description="Pesquisa textual geral (default '*' se vazio)"),
    },
)

book_item_model = swagger.model(
    "BookItem",
    {
        "external_id": fields.String(description="ID da OpenLibrary (key)"),
        "title": fields.String(description="Título"),
        "subtitle": fields.String(description="Subtítulo"),
        "author_name": fields.String(description="Autor(es)"),
        "first_publish_year": fields.String(description="Ano da primeira publicação"),
        "cover_id": fields.String(description="ID de capa (se existir)"),
    },
)

book_search_response_model = swagger.model(
    "BookSearchResponse",
    {
        "page": fields.Integer,
        "limit": fields.Integer,
        "count": fields.Integer,
        "total": fields.Integer(description="Total informado pela OpenLibrary"),
        "items": fields.List(fields.Nested(book_item_model)),
    },
)

read_payload_model = swagger.model(
    "ReadPayload",
    {
        "external_id": fields.String(required=True, description="ID retornado pela OpenLibrary (key)"),
        "note": fields.String(description="Observação opcional sobre o livro lido"),
    },
)

read_response_model = swagger.model(
    "ReadResponse",
    {
        "read_id": fields.Integer,
        "note": fields.String,
        "read_at": fields.String,
        "book": fields.Nested(book_item_model),
    },
)

read_list_item_model = swagger.model(
    "ReadListItem",
    {
        "read_id": fields.Integer,
        "note": fields.String,
        "read_at": fields.String,
        "external_id": fields.String,
        "title": fields.String,
        "subtitle": fields.String,
        "author_name": fields.String,
        "first_publish_year": fields.String,
        "cover_id": fields.String,
    },
)

read_list_response_model = swagger.model(
    "ReadListResponse",
    {
        "page": fields.Integer,
        "per_page": fields.Integer,
        "count": fields.Integer,
        "total": fields.Integer,
        "items": fields.List(fields.Nested(read_list_item_model)),
    },
)
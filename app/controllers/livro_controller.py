from flask import request
from flask_restx import Resource
from app.services.livro_service import BookService, ReadService
from app.settings.swagger import (
    book_search_filters_model,
    book_search_response_model,
    read_payload_model,
    read_response_model,
    read_list_response_model,
)


class BookController:
    @staticmethod
    def configure_routes(swagger):
        books_ns = swagger.namespace("books", description="Pesquisa de livros na OpenLibrary")
        reads_ns = swagger.namespace("reads", description="Gerenciamento de livros lidos")

        @books_ns.route("/")
        class BooksResource(Resource):
            @swagger.doc(
                "listar_livros",
                params={
                    "page": "Página (default 1)",
                    "limit": "Itens por página (default 10, máx 50)",
                    "author": "Filtro por autor",
                    "title": "Filtro por título",
                    "q": "Busca textual geral",
                },
            )
            @swagger.marshal_with(book_search_response_model)
            def get(self):
                """Lista livros paginados a partir da OpenLibrary."""
                page = max(int(request.args.get("page", 1)), 1)
                limit = min(max(int(request.args.get("limit", 10)), 1), 50)
                author = request.args.get("author")
                title = request.args.get("title")
                query = request.args.get("q")
                return BookService.search_books(author=author, title=title, query=query, page=page, limit=limit)

        @reads_ns.route("/")
        class ReadListResource(Resource):
            @swagger.doc(
                "listar_lidos",
                params={
                    "page": "Página (default 1)",
                    "per_page": "Itens por página (default 10, máx 50)",
                },
            )
            def get(self):
                """Lista livros marcados como lidos, com paginação local."""
                page = max(int(request.args.get("page", 1)), 1)
                per_page = min(max(int(request.args.get("per_page", 10)), 1), 50)
                return ReadService.list_reads(page=page, per_page=per_page)

            @swagger.doc("marcar_lido")
            @swagger.expect(read_payload_model, validate=True)
            @swagger.marshal_with(read_response_model, code=201)
            def post(self):
                """Marca um livro como lido e armazena observação opcional."""
                payload = request.json or {}
                external_id = payload.get("external_id")
                note = payload.get("note")
                if not external_id:
                    return {"message": "external_id é obrigatório."}, 400
                return ReadService.mark_as_read(external_id, note)

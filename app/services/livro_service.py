from app.clients.openlibrary_client import OpenLibraryClient
from app.notification.notification import NotificationService
from app.repositories.book_cache_repository import BookCacheRepository
from app.repositories.read_repository import ReadRepository


class BookService:
    @staticmethod
    def search_books(author: str | None, title: str | None, query: str | None, page: int, limit: int):
        # Se nenhum filtro for enviado, use busca ampla para evitar retorno vazio.
        if not (author or title or query):
            query = "*"

        try:
            response = OpenLibraryClient.search(author=author, title=title, query=query, page=page, limit=limit)
        except Exception as exc:
            return NotificationService.notify_error(f"Erro ao consultar fonte externa: {exc}", 502)

        docs = response.get("docs", [])
        num_found = response.get("numFound", len(docs))

        items = []
        for doc in docs:
            try:
                cached = BookCacheRepository.upsert_from_doc(doc)
                items.append(cached.as_dict())
            except Exception:
                # ignora documentos malformados sem interromper a lista
                continue

        return {
            "page": page,
            "limit": limit,
            "count": len(items),
            "total": num_found,
            "items": items,
        }

    @staticmethod
    def ensure_cached_book(external_id: str):
        cached = BookCacheRepository.get_by_external_id(external_id)
        if cached:
            return cached

        work = OpenLibraryClient.fetch_work(external_id)
        if not work:
            return None

        doc_like = {
            "key": f"/{external_id.lstrip('/')}",
            "title": work.get("title"),
            "subtitle": work.get("subtitle"),
            "author_name": [a.get("name") for a in (work.get("authors") or []) if a.get("name")],
            "first_publish_year": work.get("first_publish_date"),
        }
        return BookCacheRepository.upsert_from_doc(doc_like)


class ReadService:
    @staticmethod
    def mark_as_read(external_id: str, note: str | None = None):
        book = BookService.ensure_cached_book(external_id)
        if not book:
            return NotificationService.notify_error("Livro não encontrado na fonte externa.", 404)

        read_entry = ReadRepository.add_read(book, note)
        return {
            "message": "Livro marcado como lido.",
            "read_id": read_entry.id,
            "book": book.as_dict(),
            "note": read_entry.note,
            "read_at": read_entry.read_at.isoformat(),
        }, 201

    @staticmethod
    def list_reads(page: int, per_page: int):
        items, total = ReadRepository.list_reads(page, per_page)
        return {
            "page": page,
            "per_page": per_page,
            "count": len(items),
            "total": total,
            "items": [
                {
                    "read_id": r.id,
                    "note": r.note,
                    "read_at": r.read_at.isoformat(),
                    **r.book.as_dict(),
                }
                for r in items
            ],
        }

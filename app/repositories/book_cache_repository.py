from app.models.book_model import BookCache, db


class BookCacheRepository:
    @staticmethod
    def upsert_from_doc(doc: dict) -> BookCache:
        external_id = doc.get("key")
        if not external_id:
            raise ValueError("External id (key) é obrigatório para cachear o livro.")

        book = BookCache.query.filter_by(external_id=external_id).first()
        if book is None:
            book = BookCache(external_id=external_id)

        author_list = doc.get("author_name") or []
        book.title = doc.get("title")
        book.subtitle = doc.get("subtitle")
        book.author_name = ", ".join(author_list) if isinstance(author_list, list) else author_list
        book.first_publish_year = doc.get("first_publish_year")
        book.cover_id = str(doc.get("cover_i")) if doc.get("cover_i") is not None else None

        db.session.add(book)
        db.session.commit()
        return book

    @staticmethod
    def get_by_external_id(external_id: str) -> BookCache | None:
        return BookCache.query.filter_by(external_id=external_id).first()


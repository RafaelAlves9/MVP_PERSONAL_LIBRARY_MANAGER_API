from app.models.book_model import ReadBook, db


class ReadRepository:
    @staticmethod
    def add_read(book, note: str | None = None) -> ReadBook:
        existing = ReadBook.query.filter_by(book_id=book.id).first()
        if existing:
            if note is not None:
                existing.note = note
                db.session.commit()
            return existing

        read_entry = ReadBook(book=book, note=note)
        db.session.add(read_entry)
        db.session.commit()
        return read_entry

    @staticmethod
    def list_reads(page: int, per_page: int):
        query = ReadBook.query.order_by(ReadBook.read_at.desc())
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        total = query.count()
        return items, total


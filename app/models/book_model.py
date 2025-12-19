from datetime import datetime
from app.models.database import db


class BookCache(db.Model):
    __tablename__ = "book_cache"

    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(128), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255))
    author_name = db.Column(db.String(255))
    first_publish_year = db.Column(db.Integer)
    cover_id = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def as_dict(self):
        return {
            "external_id": self.external_id,
            "title": self.title,
            "subtitle": self.subtitle,
            "author_name": self.author_name,
            "first_publish_year": self.first_publish_year,
            "cover_id": self.cover_id,
        }


class ReadBook(db.Model):
    __tablename__ = "read_books"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book_cache.id"), nullable=False, unique=True)
    note = db.Column(db.Text)
    read_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    book = db.relationship(
        BookCache,
        backref=db.backref("read_entry", uselist=False),
        lazy="joined",
    )


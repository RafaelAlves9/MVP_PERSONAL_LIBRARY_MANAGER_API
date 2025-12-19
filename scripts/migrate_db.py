"""
Script simples para alinhar o schema do SQLite atual com os modelos vigentes.
Faz backup opcional do arquivo e executa drop_all/create_all.

Uso:
  export DATABASE_URL=sqlite:////app/instance/books.db  # ou caminho desejado
  python scripts/migrate_db.py
"""

import os
import shutil
from pathlib import Path

from run import app, db  # type: ignore


def backup_database(db_uri: str) -> Path | None:
    if not db_uri.startswith("sqlite:///"):
        return None

    db_path = db_uri.replace("sqlite:///", "", 1)
    path = Path(db_path)
    if not path.exists():
        return None

    backup_path = path.with_suffix(path.suffix + ".bak")
    shutil.copy(path, backup_path)
    return backup_path


def migrate():
    db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
    backup = backup_database(db_uri)

    with app.app_context():
        db.drop_all()
        db.create_all()

    if backup:
        print(f"Backup criado em: {backup}")
    print("Migração concluída: schema atualizado para BookCache e ReadBook.")


if __name__ == "__main__":
    migrate()


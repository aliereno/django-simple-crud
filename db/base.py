import os
from datetime import datetime
from pathlib import Path

from peewee import DateTimeField, Model, SqliteDatabase

BASE_DIR = Path(__file__).resolve().parent.parent
database_name = BASE_DIR / os.environ.get("DB_PATH", "db.sqlite3")
db = SqliteDatabase(database_name)


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db


def create_tables(model, *extra_models):
    models = model.__subclasses__()

    # delete BaseModel
    if BaseModel in models:
        models.pop(models.index(BaseModel), None)

    for m in extra_models:
        models.append(m)

    db.create_tables(models)

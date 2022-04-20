from book import models
from db.base import create_tables

create_tables(models.BaseModel, models.Book.authors.get_through_model())

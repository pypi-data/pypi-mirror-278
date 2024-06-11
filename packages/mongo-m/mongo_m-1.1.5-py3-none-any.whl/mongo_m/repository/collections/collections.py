from pymongo import MongoClient
from pymongo.database import Database
from .models import Schema
from .query import get_fields
from typing import Generator

__all__ = ["find_collections", "get_fields_collections"]


def find_collections(client: MongoClient, db_name: str) -> Database:
    db = client[db_name]
    return db


def get_fields_collections(db: Database) -> Generator[Schema, None, None]:
    query_field = get_fields()
    for collection_name in db.list_collection_names():
        collection = db.get_collection(collection_name)
        batches = list(collection.aggregate(query_field))
        collection_data = Schema(name=collection_name)
        [collection_data.fields.add(batch['field']) for batch in batches]
        yield collection_data

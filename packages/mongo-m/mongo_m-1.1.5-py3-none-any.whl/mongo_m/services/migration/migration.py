import pymongo
from pymongo.database import Database
from mongo_m.core import MongoDB, get_config
from mongo_m.repository import collections
from mongo_m.repository.collections.models import Query
from .file import FileMigration

__all__ = [
    'connect_to_mongo',
    'get_collections',
    'get_database',
    'delete_fields',
    'add_fields',
    'screening_fields'
]


def connect_to_mongo() -> pymongo.MongoClient:
    """
    Connects to a MongoDB database using environment variables for configuration.

    Returns:
    - pymongo.database.Database: The connected MongoDB database.
    """
    config = get_config()
    return MongoDB(config.get("MONGO", "host"),
                   int(config.get("MONGO", "port")),
                   config.get("MONGO", "user"),
                   config.get("MONGO", "password"))


def get_collections(client: pymongo.MongoClient):
    db = get_database(client)
    return collections.get_fields_collections(db)


def get_database(client: pymongo.MongoClient):
    config = get_config()
    db_name = config.get("MONGO", "database")
    db = collections.find_collections(client, db_name)
    return db


def delete_fields(db: Database, collection_name: str, params):
    if params.empty:
        return
    try:
        db.get_collection(collection_name).update_many({"$or": params.query}, {"$unset": params.fields})
        print(f"Удаление полей {params.fields}")
    except Exception as e:
        print(e)


def add_fields(db: Database, collection_name: str, params):
    if params.empty:
        return
    try:
        db.get_collection(collection_name).update_many({"$or": params.query}, {"$set": params.fields})
        print(f"Добавление полей {params.fields}", sep="\n")
    except Exception as e:
        print(e)


def screening_fields(client: pymongo.MongoClient):
    """
    Опеределение расхождений в полях между базой данных и моделькой
    :param client:
    :type client:
    :return:
    :rtype:
    """
    collections_migration = FileMigration.get_migration()
    for collection in get_collections(client):
        if collection.name in collections_migration:
            fields = set(collections_migration[collection.name].keys())
            # Симметрическая разность множеств
            disjunctive = fields ^ collection.fields
            if "_id" in disjunctive:
                disjunctive.remove("_id")
            delete = Query()
            add = Query()
            for field in disjunctive:
                if field in fields:
                    add.query.append({field: {"$exists": False}})
                    add.fields[field] = collections_migration[collection.name][field]
                    add.empty = False
                if field not in fields and collection.fields:
                    delete.query.append({field: {"$exists": True}})
                    delete.fields[field] = ""
                    delete.empty = False
            yield collection.name, add, delete

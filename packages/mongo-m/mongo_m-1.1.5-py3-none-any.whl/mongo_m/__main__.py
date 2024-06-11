import sys
import asyncio
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
from .core import create_file_ini, get_config
from .services.migration import (
    FileMigration, connect_to_mongo,
    add_fields, delete_fields,
    screening_fields,
    get_database
)

load_dotenv()
PATH = Path(__file__).parent.resolve()


def update_migration(client: MongoClient, type_action: bool):
    """
    Выполнение миграции
    :param client:
    :type client:
    :param type_action: bool True добавление полей False удаление
    :type type_action:
    :return:
    :rtype:
    """
    db = get_database(client)
    for collection_name, add, delete in screening_fields(client):
        if type_action:
            add_fields(db, collection_name, add)
        else:
            delete_fields(db, collection_name, delete)


async def create_migration():
    config = get_config()
    module_path = config.get("MONGO", "module_path")
    migration_file = await FileMigration.make_migration(module_path)
    FileMigration.update_migration_file(migration_file)


async def main():
    FileMigration.create_migration_catalog()
    params = tuple(sys.argv[1:])
    client = None
    try:
        if params[0] == "create-migration":
            await create_migration()
        elif params[0] == "update-migration":
            client = connect_to_mongo()
            action = None

            if params[1] == '-a':
                action = True
            elif params[1] == '-d':
                action = False

            if action is not None:
                update_migration(client, action)
        elif params[0] == "init":
            create_file_ini()
    except Exception as e:
        print(e)
    finally:
        if client is not None:
            client.close()

if __name__ == "__main__":
    asyncio.run(main())

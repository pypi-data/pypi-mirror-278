import os
import json
import hashlib
from pathlib import Path
from mongo_m.core.inspect_module import make_module, inspect_module
from mongo_m.core import check_catalog, create_catalog

__all__ = ['FileMigration']


class FileMigration:

    PATH_MIGRATION = Path(f"{os.getcwd()}/migration")
    PATH_JSON = Path(f"{os.getcwd()}/migration/update.json")

    @classmethod
    def create_migration_catalog(cls):
        if not check_catalog(cls.PATH_MIGRATION.name):
            create_catalog(cls.PATH_MIGRATION.name)

    @classmethod
    async def make_migration(cls, module_path: str):
        modules = {}
        async for module in make_module(module_path):
            module = inspect_module(module)
            if module != {}:
                for name, value in module.items():
                    modules[name] = {
                        name: value,
                    }
        modules = json.dumps(list(modules.values()), indent=4)
        hash_name = hashlib.md5(modules.encode())
        file_name = f"{hash_name.hexdigest()}.json"
        with open(file=f"{cls.PATH_MIGRATION}/{file_name}", mode='w') as f:
            f.write(modules)
        return file_name

    @classmethod
    def update_migration_file(cls, file_migration: str):
        """
        Обновляет стек выполненых миграций
        """
        try:
            with open(file=cls.PATH_JSON, mode="r+") as f:
                file_data = f.read()
                items = json.loads(file_data)

                if len(items) == 0:
                    items.append(file_migration)
                elif file_migration != items[-1]:
                    items.append(file_migration)

                f.truncate(0)
                f.seek(0)
                f.write(json.dumps(items, indent=4))
                f.seekable()

        except FileNotFoundError:
            with open(file=cls.PATH_JSON, mode="w") as f:
                f.write(json.dumps([file_migration], indent=4))

    @classmethod
    def get_last_migration(cls):
        with open(file=cls.PATH_JSON, mode="r") as f:
            file_data = f.read()
            items = json.loads(file_data)
            if len(items) == 0:
                raise FileNotFoundError("File migration not found")
            return items[-1]

    @classmethod
    def get_migration(cls):
        last_migration = cls.get_last_migration()
        result = {}
        with open(file=f"{cls.PATH_MIGRATION}/{last_migration}", mode="r") as f:
            file_data = f.read()
            items = json.loads(file_data)
            for item in items:
                key = list(item.keys())[0]
                result[key] = item[key]
        return result

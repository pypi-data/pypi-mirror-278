import os
import sys
import importlib
import inspect
import datetime
from pathlib import Path
from .utils import get_default_value
from typing import AsyncIterable

__all__ = ["make_module", "inspect_module", "get_module"]


async def make_module(module_path: str) -> AsyncIterable:
    """
    Asynchronously creates a module from the given `module_path`.

    Args:
        module_path (str): The path to the module.

    Yields:
        module: The module object.

    Raises:
        ModuleNotFoundError: If the module cannot be found.

    Returns:
        None: If the function completes successfully.
    """
    path = f"{os.getcwd()}/{module_path}".replace("\\", "/")
    print(path, os.path.isdir(path))
    if os.path.isdir(path):
        files = make_module_dir(path, module_path)
    else:
        path_module = module_path.replace("/", ".")
        files = [path_module]
    for name in files:
        try:
            module = get_module(name)
            yield module
        except ModuleNotFoundError as e:
            print(e)
            continue
    return


def make_module_dir(path: str, module_path: str):
    """
    Generate a list of module names based on the files in the given directory.

    Args:
        path (str): The path to the directory.
        module_path (str): The module path.

    Returns:
        list: A list of module names.
    """
    path_module = Path(path)
    module_path = module_path.replace("/", ".")
    result = []
    for file in filter(lambda x: x not in {"__init__.py", "__pycache__"}, os.listdir(path_module)):
        module = f"{module_path}.{file.replace('.py', '')}"
        result.append(module)
    return result


def get_module(module_path: str):
    """
    This function imports a module if it is not already in sys.modules.
    Args:
        module_path (str): The path of the module to be imported.
    Returns:
        The imported module.
    """
    if module_path in sys.modules:
        return sys.modules[module_path]
    return importlib.import_module(module_path)


def inspect_module(module) -> dict:
    """
    Состоявляем поля модели на основе класса
    """
    models = {}
    for name, obj in inspect.getmembers_static(module, inspect.isclass):
        print(dir(obj))
        table_name = None
        if '__table_name__' in dir(obj):
            table_name = obj.__table_name__
        elif '__tablename__' in dir(obj):
            table_name = obj.__tablename__
        if table_name is not None:
            if table_name in models:
                continue
            params = {}
            for values in inspect.signature(obj).parameters.values():
                if values.name == 'id':
                    continue
                # Определение параметров по дефолту
                if not inspect.isclass(values.annotation):
                    """
                        Парсинг типов данных и установка значиний по умолчанию для создания схемы
                        пример 'bool | None' or 'int | str | None'
                        Берется первый элемент из массива
                    """
                    annotated_types = str(values.annotation).split("|")
                    annotated_types = annotated_types[0].strip()
                else:
                    annotated_types = values.annotation.__name__

                if values.default is inspect._empty:
                    default_value = get_default_value(annotated_types)
                else:
                    default_value = values.default
                    if default_value.__class__ is datetime.datetime:
                        default_value = default_value.strftime("%Y-%m-%d %H:%M:%S.%f")

                params[values.name] = default_value
            models[table_name] = params
    return models

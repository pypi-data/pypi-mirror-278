"""
    Создание и удаление директорий программы и файлов
"""

import os

__all__ = ["check_catalog", "create_catalog"]


def check_catalog(catalog: str) -> bool:
    """
    Проверка существования директории
    """
    return os.path.exists(catalog)


def create_catalog(catalog: str) -> None:
    """
    Создание директории
    """
    if not check_catalog(catalog):
        os.mkdir(catalog)

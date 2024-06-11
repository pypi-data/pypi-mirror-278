from pydantic import BaseModel
from bson import ObjectId
from enum import Enum
from datetime import datetime


class DataTypes(Enum):
    STRING = str
    INT = int
    FLOAT = float
    BOOLEAN = bool
    DATE = datetime.now
    OBJECTID = ObjectId
    ARRAY = list
    OBJECT = dict
    NULL = None


class Schema(BaseModel):
    name: str
    fields: set[str] = set()


class Query(BaseModel):
    query: list = []
    fields: dict = {}
    empty: bool = True

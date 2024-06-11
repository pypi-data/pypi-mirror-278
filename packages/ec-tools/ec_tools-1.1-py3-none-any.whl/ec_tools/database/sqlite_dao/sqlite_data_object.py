import abc
import dataclasses
from typing import List

from ec_tools.dataclass import DataclassExt


@dataclasses.dataclass
class SqliteDataObject(abc.ABC, DataclassExt):
    """
    - primary_keys: define the primary keys of the object
    - extra_indexes: append extra indexes with default index (primary keys)
    - unique_keys: append extra unique constraints with default unique constraint (primary keys)
    - use _load__xxx to override loading json field to class field
    - use _dump__xxx to override dumping class field to json field
    """

    @classmethod
    @abc.abstractmethod
    def primary_keys(cls) -> List[str]:
        ...

    @classmethod
    def extra_indexes(cls) -> List[List[str]]:
        return []

    @classmethod
    def unique_keys(cls) -> List[List[str]]:
        return []

    @classmethod
    def table_name(cls) -> str:
        return cls.__name__

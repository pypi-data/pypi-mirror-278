import dataclasses

from typing import List, Dict, Any, Callable

from ec_tools.database.utils.dataclass_utils import get_default, DefaultFormat


@dataclasses.dataclass
class DataclassExt:
    def __getitem__(self, key: str):
        return self.__dict__.get(key)

    def __setitem__(self, key: str, value: Any):
        self.__dict__[key] = value

    def as_json(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

    @classmethod
    def field_map(cls) -> Dict[str, dataclasses.Field]:
        return {field.name: field for field in cls.fields()}

    @classmethod
    def fields(cls) -> List[dataclasses.Field]:
        return list(dataclasses.fields(cls))

    @classmethod
    def field_names(cls) -> List[str]:
        return [field.name for field in dataclasses.fields(cls)]

    @classmethod
    def loads(cls, json_obj: Dict[str, Any]) -> "DataclassExt":
        function_mapping = cls._customized_mapping_function("_load__")
        return cls(
            **{
                field.name: function_mapping[field.name](json_obj.get(field.name, None))
                for field in cls.fields()
            }
        )

    def dumps(self) -> Dict[str, Any]:
        function_mapping = self._customized_mapping_function("_dump__")
        return {
            field.name: function_mapping[field.name](getattr(self, field.name))
            for field in dataclasses.fields(self)
        }

    @classmethod
    def _customized_mapping_function(
        cls, prefix: str
    ) -> Dict[str, Callable[[Any], Any]]:
        all_functions = {
            item: getattr(cls, item)
            for item in dir(cls)
            if isinstance(getattr(cls, item), Callable)
        }
        return {
            field.name: all_functions.get(
                prefix + field.name, DefaultFormat(field).format
            )
            for field in cls.fields()
        }

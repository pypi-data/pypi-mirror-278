from typing import Type, Iterable, Dict

from antipickle.base import AbstractAdapter, wrap


class DataclassAdapter(AbstractAdapter):
    typestring = "dataclass"

    def __init__(self, name2class: Dict[str, Type]):
        self.name2class = name2class
        self.class2name = {v: k for k, v in self.name2class.items()}

    def check_type(self, obj):
        # we intentionally ignore inherited classes
        return type(obj) in self.class2name

    def to_dict(self, obj):
        from dataclasses import fields

        return {
            "classname": self.class2name[type(obj)],
            # we don't use asdict, because it doesn't reverse that simple (and it is recursive)
            "data": {field.name: wrap(getattr(obj, field.name)) for field in fields(obj)},
        }

    def from_dict(self, d):
        classobj = self.name2class[d["classname"]]
        return classobj(**d["data"])


class PydanticAdapter(AbstractAdapter):
    typestring = "pydantic"

    def __init__(self, name2pydantic_class: Dict[str, Type]):
        self.name2class = name2pydantic_class
        self.class2name = {v: k for k, v in self.name2class.items()}

    def check_type(self, obj):
        # we intentionally ignore inherited classes
        return type(obj) in self.class2name

    def to_dict(self, obj):
        return {
            "classname": self.class2name[type(obj)],
            "data": {k: wrap(v) for k, v in obj.dict().items()},
        }

    def from_dict(self, d):
        classobj = self.name2class[d["classname"]]
        return classobj(**d["data"])


class SkipSerialization(AbstractAdapter):
    typestring = "skipped"

    def __init__(self, skipped_types: Iterable[Type]):
        self.skipped_types = set(skipped_types)

    def check_type(self, obj):
        # we intentionally ignore inherited classes
        return type(obj) in self.skipped_types

    def to_dict(self, obj):
        return {
            "skipped": True,
        }

    def from_dict(self, d):
        return "skipped, as specified during serialization"

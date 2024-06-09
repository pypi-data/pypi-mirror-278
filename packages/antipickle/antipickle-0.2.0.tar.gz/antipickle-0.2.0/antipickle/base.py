"""
Main classes/functions used for conversion.
"""

from __future__ import annotations
import dataclasses
import sys
import typing
from typing import Any, Optional, Dict

# special key in dictionary.
# Its presence means it is a custom type and should be processed by package
# It was selected because of being a rarely used ASCII symbol.
MAGIC_KEY = "\x7f"

"""
We use wrapper (LazyWrapper) to wrap every data component
except for the most trivial ones (ints, floats, str, ...)

Thus each time serializer meets wrapper, it asks how the object should be processed.
We provide such hooks for serializers / deserializers.
Hook scans for available (de)serializers for this type and applies the right one.
"""

NoneType: Any = type(None)


def wrap(obj):
    if isinstance(obj, (str, float, int, bool, bytes, NoneType)):
        return obj

    if isinstance(obj, list):
        return [wrap(x) for x in obj]
    return LazyWrapper(obj=obj)


@dataclasses.dataclass
class LazyWrapper:
    obj: typing.Any


class TypeMatcher:
    def __init__(self):
        self.adapters: Dict[str, AbstractAdapter] = {}
        self.type2adapter: Dict[Any, AbstractAdapter] = {}
        self.serialization_stack = set()

    def register_adapter(self, adapter: AbstractAdapter):
        assert isinstance(adapter, AbstractAdapter)
        assert adapter.typestring not in self.adapters
        self.adapters[adapter.typestring] = adapter

    def _serialize_object(self, x):
        t = type(x)
        x_id = id(x)
        assert x_id not in self.serialization_stack
        self.serialization_stack.add(x_id)

        if type(x) not in self.type2adapter:
            for adapter in self.adapters.values():
                if adapter.package_name is not None and adapter.package_name not in sys.modules:
                    # module wasn't previously loaded
                    continue

                if adapter.check_type(x):
                    self.type2adapter[t] = adapter
                    break
            else:
                raise RuntimeError(f"Serialization for type {t} not available.")
        adapter = self.type2adapter[t]
        result = adapter.to_dict(x)
        result[MAGIC_KEY] = adapter.typestring
        self.serialization_stack.remove(x_id)
        return result

    def _deserialize_object(self, x: dict) -> Any:
        assert isinstance(x, dict) and MAGIC_KEY in x

        typestring = x[MAGIC_KEY]
        convertor = self.adapters[typestring]

        if convertor is None:
            raise RuntimeError(f"Problems: adapter for {typestring} not found. Object: {x}")
        return convertor.from_dict(x)

    def serialize_helper(self, x):
        """
        Serialize helper should be passed as a hook to serialization to msgpack or downstream protocol
        """
        assert isinstance(x, LazyWrapper)
        if isinstance(x.obj, dict):
            return pack_dict(x.obj)
        else:
            return self._serialize_object(x.obj)

    def deserialize_helper(self, x):
        """
        Deserialize helper should be passed as a hook to serialization to msgpack or downstream protocol
        """
        if not isinstance(x, dict):
            return x
        elif MAGIC_KEY not in x:
            # usual dictionary
            return x
        else:
            return self._deserialize_object(x)


class AbstractAdapter:
    """
    Adapters should implement this interface.
    """

    package_name: Optional[str] = None
    typestring: str

    # adapter may introduce additional fields to configure save/load
    # if it is unavoidable

    def check_type(self, obj):
        raise NotImplementedError()

    def to_dict(self, obj) -> Dict[str, Any]:
        raise NotImplementedError()

    def from_dict(self, d: Dict[str, Any]):
        raise NotImplementedError()


def pack_dict(d):
    if all(isinstance(x, str) for x in d) and (MAGIC_KEY not in d):
        return {k: wrap(v) for k, v in d.items()}
    return {
        MAGIC_KEY: "dict",
        "k": [wrap(k) for k in d.keys()],
        "v": [wrap(v) for v in d.values()],
    }


class DictAdapter(AbstractAdapter):
    typestring = "dict"

    # this adapter is exceptional
    # to_dict can't be implemented, we use it only during unpacking.
    # For packing use pack_dict
    def check_type(self, obj):
        return False

    def to_dict(self, obj) -> Dict[str, Any]:
        raise NotImplementedError("This will never be called")

    def from_dict(self, d):
        k, v = d["k"], d["v"]
        return dict(zip(k, v))

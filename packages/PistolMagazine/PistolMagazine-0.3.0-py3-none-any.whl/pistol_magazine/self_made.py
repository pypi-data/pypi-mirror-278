from pistol_magazine.base import _BaseField
from pistol_magazine.datetime import Datetime
from pistol_magazine.dict import Dict
from pistol_magazine.float import Float
from pistol_magazine.int import Int
from pistol_magazine.list import List
from pistol_magazine.str import Str, StrTimestamp
from pistol_magazine.timestamp import Timestamp
from .provider import fake


class _MetaMocker(type):
    order = {}

    def __new__(mcs, clsname, bases, clsdict):
        order = {key: value for key, value in clsdict.get("__annotations__", {}).items() if
                 issubclass(value, _BaseField) and key not in clsdict.keys()}
        models = {
            key: value() for key, value in order.items()
        }
        for key, value in clsdict.items():
            if isinstance(value, _BaseField):
                models[key] = value
        clsdict["models"] = Dict(models)
        new_cls = type.__new__(mcs, clsname, bases, clsdict)
        return new_cls


class DataMocker(metaclass=_MetaMocker):
    models: Dict or List = None

    def __init__(self, models=None):
        if models:
            self.models = models

    @classmethod
    def read_value(cls, value):
        if isinstance(value, int):
            result = Timestamp.match(value)
            if result is not None:
                return Timestamp(result)
            else:
                return Int()
        elif isinstance(value, float):
            return Float()
        elif isinstance(value, str):
            if Datetime.match(value) is not None:
                return Datetime(Datetime.match(value))
            elif StrTimestamp.match(value) is not None:
                return StrTimestamp(StrTimestamp.match(value))
            else:
                return Str.match(value)
        elif isinstance(value, dict):
            return cls.data_to_model(value)
        elif isinstance(value, list):
            return cls.data_to_model(value)

    @classmethod
    def data_to_model(cls, data: dict or list):
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                result[key] = cls.read_value(value)
            return Dict(result)
        elif isinstance(data, list):
            result = []
            for value in data:
                result.append(cls.read_value(value))
            return List(result)
        else:
            raise ValueError(f"Unsupported type{data} {type(data)}")

    @classmethod
    def load_value(cls, value):
        if isinstance(value, dict):
            return cls.model_to_data(value)
        elif isinstance(value, list):
            return cls.model_to_data(value)
        else:
            class_name, *args = value.split("_")
            return Int.name_map[class_name](*args)

    @classmethod
    def model_to_data(cls, data: dict or list) -> Dict or List:
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                result[key] = cls.load_value(value)
            return Dict(result)
        elif isinstance(data, list):
            result = []
            for value in data:
                result.append(cls.load_value(value))
            return List(result)
        else:
            raise ValueError(f"Unsupported type{data} {type(data)}")

    def get_datatype(self):
        return self.models.get_datatype()

    def mock(self, to_json: bool = False):
        return self.models.mock(to_json=to_json)

    @classmethod
    def __call__(cls, *args, **kwargs):
        return cls.models(*args, **kwargs)

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return getattr(fake, name)


class ProviderField(_BaseField):
    def __init__(self, provider_method):
        self.provider_method = provider_method

    def mock(self):
        return self.provider_method()

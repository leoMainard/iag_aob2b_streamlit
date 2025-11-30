import os
from enum import Enum

class Environnement:
    _configuration = None

    @classmethod
    def _load_config(cls):
        if cls._configuration is None:
            cls._configuration = {
                "ENV_VAR_EXEMPLE": os.getenv("ENV_VAR_EXEMPLE"),
            }

    @classmethod
    def config(cls, name):
        cls._load_config()
        try:
            return cls._configuration[name]
        except KeyError:
            raise KeyError(f"Configuration '{name}' not found.")


class ExempleEnum(Enum):

    VALUE1 = "value1"
    VALUE2 = "value2"

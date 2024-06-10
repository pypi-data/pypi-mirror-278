import os
import yaml
from .Exceptions import InvalidPropertyError, EmptyValueProperty, KeyExistsError

class ConfigSchema:
    def __init__(self, default_schema=None, filepath=None, default_config=None) -> None:
        if default_schema is None:
            default_schema = {}
        
        if not isinstance(default_schema, dict):
            raise InvalidPropertyError("default_schema must be a dictionary.")
        
        self.properties = default_schema
        self.current_idx = -1

        # Load default configuration if specified or from file
        if default_config and os.path.isfile(default_config):
            self.load(default_config)
        elif filepath and os.path.isfile(filepath):
            self.load(filepath)
        elif not filepath:
            config_file = next((item for item in os.listdir() if item in ["config.yaml", "config.yml"]), None)
            if config_file and os.path.getsize(config_file) > 0:
                self.load(config_file)

    def __str__(self) -> str:
        return str(self.properties)

    def __iter__(self):
        self.current_idx = -1
        return self

    def __next__(self):
        self.current_idx += 1
        if self.current_idx < len(self.properties):
            return list(self.properties.items())[self.current_idx]
        raise StopIteration

    def add(self, nkey, nvalue=None, override=True) -> None:
        if isinstance(nkey, dict):
            if override:
                self.properties.update(nkey)
            else:
                for key, value in nkey.items():
                    if key not in self.properties:
                        self.properties[key] = value
        else:
            if nvalue is None:
                raise EmptyValueProperty("Value cannot be None.")
            if not override and nkey in self.properties:
                return  # Simply return without updating if key exists and override is False
            self.properties[nkey] = nvalue

    def get(self, key, strict=False):
        try:
            return self.properties[key]
        except KeyError as e:
            if strict:
                raise KeyError(f"The key '{key}' does not exist.") from e

    def remove(self, key, strict=False):
        try:
            self.properties.pop(key)
        except KeyError as e:
            if strict:
                raise KeyError(f"The key '{key}' does not exist.") from e

    def load(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"The file '{filepath}' does not exist.")
        
        with open(filepath, "r") as fh:
            config = yaml.safe_load(fh) or {}
            if not self.properties or len(self.properties) <= 1:
                self.properties = config
            else:
                self.properties.update(config)

    def items(self):
        return self.properties.items()
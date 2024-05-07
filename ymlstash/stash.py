import yaml
import os

from dataclasses import asdict, fields
from pathlib import Path


class YmlStash:
    def __init__(self, clazz, path, file_suffix="yml", unsafe=False):
        self.clazz = clazz
        self.path = Path(path)
        self.file_suffix = f".{file_suffix}"
        self.yaml_loader = yaml.SafeLoader
        self._validate()

    def _validate(self):
        if not self.path.exists():
            raise Exception(f"Path {self.path} does not exist and cannot be used")

        key_field = getattr(self.clazz, "key", None)
        field_names = [f.name for f in fields(self.clazz)]
        if key_field and key_field not in field_names:
            raise Exception(f"Dataclass {self.clazz} has no key field '{key_field}'")

    def _get_path(self, key):
        return self.path / f"{key}{self.file_suffix}"

    def load(self, key):
        with open(self._get_path(key)) as f:
            y = yaml.load(f.read(), Loader=self.yaml_loader)
        return self.clazz(**y)

    def save(self, obj, key=None):
        if not key:
            key_field = self.clazz.key
            if not key_field:
                raise Exception("Cannot save object without a key or key field")
            key = getattr(obj, key_field)
        with open(self._get_path(key), "w") as f:
            f.write(yaml.dump(asdict(obj)))

    def _list_files(self):
        return [f for f in os.listdir(self.path) if f.endswith(self.file_suffix)]

    def list_keys(self):
        return [f.replace(self.file_suffix, "") for f in self._list_files()]

    def drop(self):
        for f in self._list_files():
            if f.endswith(self.file_suffix):
                os.remove(self.path / f)

import yaml
import os

from dataclasses import asdict
from pathlib import Path


class YmlStash:
    def __init__(self, clazz, path, file_suffix="yml", unsafe=False):
        self.clazz = clazz
        self.path = Path(path)
        self.file_suffix = f".{file_suffix}"
        self.yaml_loader = yaml.SafeLoader

    def _get_path(self, key):
        return self.path / f"{key}{self.file_suffix}"

    def load(self, key):
        with open(self._get_path(key)) as f:
            y = yaml.load(f.read(), Loader=self.yaml_loader)
        return self.clazz(**y)

    def save(self, key, obj):
        with open(self._get_path(key), "w") as f:
            f.write(yaml.dump(asdict(obj)))

    def _list_all_files(self):
        return [f for f in os.listdir(self.path) if f.endswith(self.file_suffix)]

    def list_all_keys(self):
        return [f.replace(self.file_suffix, "") for f in self._list_all_files()]

    def drop(self):
        for f in self._list_all_files():
            if f.endswith(self.file_suffix):
                os.remove(self.path / f)

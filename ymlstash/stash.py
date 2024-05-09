import yaml
import os

from dataclasses import asdict, fields, is_dataclass
from pathlib import Path


class YmlStash:
    def __init__(
        self,
        model,
        path,
        file_suffix="yml",
        unsafe=False,
        filter_none=False,
    ):
        self.model = model
        self.path = Path(path)
        self.file_suffix = f".{file_suffix}"
        self.yaml_loader = yaml.SafeLoader
        self.filter_none = filter_none
        self._validate()

    def _validate(self):
        if not self.path.exists():
            raise Exception(f"Path {self.path} does not exist and cannot be used")

        if not is_dataclass(self.model):
            raise Exception(f"Class {self.model} is not a dataclass")

        key_field = getattr(self.model, "key", None)
        field_names = [f.name for f in fields(self.model)]
        if key_field and key_field not in field_names:
            raise Exception(f"Dataclass {self.model} has no key field '{key_field}'")

    def _get_path(self, key):
        return self.path / f"{key}{self.file_suffix}"

    def load(self, key):
        with open(self._get_path(key)) as f:
            y = yaml.load(f.read(), Loader=self.yaml_loader)
        return self.model(**y)

    def save(self, obj, key=None):
        if not key:
            key_field = self.model.key
            if not key_field:
                raise Exception("Cannot save object without a key or key field")
            key = getattr(obj, key_field)
        with open(self._get_path(key), "w") as f:
            obj_dict = asdict(obj)
            if self.filter_none:
                obj_dict = {k: v for (k, v) in obj_dict.items() if v is not None}
            f.write(
                yaml.dump(
                    obj_dict,
                    allow_unicode=True,
                    default_flow_style=False,
                    sort_keys=False,
                )
            )

    def delete(self, key):
        try:
            os.remove(self._get_path(key))
        except FileNotFoundError:
            raise Exception(
                f"Attempting to delete key '{key}' which was not found in stash"
            )

    def exists(self, key):
        return self._get_path(key).exists()

    def _list_files(self):
        return [f for f in os.listdir(self.path) if f.endswith(self.file_suffix)]

    def list_keys(self):
        return [f.replace(self.file_suffix, "") for f in self._list_files()]

    def drop(self):
        for key in self.list_keys():
            self.delete(key)

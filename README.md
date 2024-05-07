# ymlstash

A simple ORM-like utility for operating on local YAML files via Python dataclasses.

## Install

Package is published on PyPI - https://pypi.org/project/ymlstash/

Install from pip or your favorite package manager:

```bash
$ pip install ymlstash
```

## Usage

Define a dataclass:

```python
from dataclasses import dataclass
from typing import ClassVar

@dataclass
class User:
    name: str
    age: int
    active: bool
    key: ClassVar[str] = "name"
```

Note the special `key` field which is used to denote that `name` should be used as the primary key field. If an object has `name: "foo"`, it will be saved as `foo.yml` in the stash root directory.

Instantiate a new object:

```python
user = User(name="yuval", age=42, active=True)
```

Save it to file:

```python
from ymlstash import YmlStash

stash = YmlStash(User, "path/to/db")
stash.save(user)
```

This will create a `yuval.yml` file in the stash root directory.

When saving to file, a `key` field must be present on the dataclass, otherwise an explicit `key` must be passed:

```python
stash.save(obj, key="custom-key")
```

Load from file:

```python
user = stash.load("yuval")
```

List all keys existing in stash:

```python
keys = stash.list_keys()
```

## License

[MIT](LICENSE)

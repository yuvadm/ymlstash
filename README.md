# ymlstash

A simple ORM-like utility for operating on local YAML files via Python dataclasses.

In the context of this library, a *stash* is a diretory in the filesystem that holds many `.yml` files that all adhere to the same structure.

`ymlstash` simplifies the management of such a basic database of files.

## Install

Package is published on PyPI - https://pypi.org/project/ymlstash/

Install from pip or your favorite package manager:

```bash
$ pip install ymlstash
```

## Usage

Start by defining your model as a dataclass:

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

### Primary Keys

Each model **must** include a primary key that will be used as the entry filename to uniquely access each record. 

The recommended way do to this is with the special `key` field which is used to denote that `name` should be used as the primary key field. If an object has `name: "foo"`, it will be saved as `foo.yml` in the stash root directory.

### Actions

Instantiate a new object:

```python
user = User(name="yuval", age=42, active=True)
```

Save it to file:

```python
from ymlstash import YmlStash

stash = YmlStash(User, "path/to/db")  # path can either be a string or Path() object
stash.save(user)
```

This will create a `yuval.yml` file in the stash root directory.

If the `key` field is not present on the dataclass, an explicit `key` must be passed:

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

Delete a key:

```python
stash.delete("foo")
```

Check for key existence:

```python
stash.exists("foo")
```

Drop all files (careful, this deletes everything):

```python
stash.drop()
```

## License

[MIT](LICENSE)

# ymlstash

A simple ORM-like utility for operating on local YAML files via Python dataclasses.

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

Note the `key` field which is used to denote that `name` should be used as the primary key field.

Instantiate a new object:

```python
user = User(name="yuval", age=42, active=True)
```

Save it to file:

```python
from ymlstash import YmlStash

stash = YmlStash(User, "path/to/db")
stash.save("yuval", user)
```

Load from file:

```python
user = stash.load("yuval")
```

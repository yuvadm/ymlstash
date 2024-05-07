# ymlstash

A simple ORM-like utility for operating on local YAML files via Python dataclasses.

Define a dataclass:

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    active: bool
```

Instantiate a new object:

```python
user = User(name="yuval", age=42, active=True)
```

Save it to file:

```python
from ymlstash import YmlStash

stash = YmlStash("path/to/db")
stash.save(user)
```

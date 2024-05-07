# ymlstash

A simple ORM-like utility for operating on local YAML files via Python dataclasses.

Define a dataclass:

```python
@dataclass
class User:
    name: str
    age: int
    active: bool
```

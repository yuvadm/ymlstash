from pathlib import Path
from ymlstash import YmlStash
from dataclasses import dataclass


@dataclass
class User:
    name: str
    age: int


def test_stash_path():
    stash = YmlStash(User, "foo")
    assert stash.path == Path("foo")
    stash = YmlStash(User, Path("foo"))
    assert stash.path == Path("foo")


def test_stash():
    stash = YmlStash(User, "/tmp/")
    yuval = User(name="yuval", age=42)
    stash.save("foo", yuval)
    assert stash.list_all_keys() == ["foo"]
    obj = stash.load("foo")
    assert obj == yuval
    stash.drop()
    assert stash.list_all_keys() == []

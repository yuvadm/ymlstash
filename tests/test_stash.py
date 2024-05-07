import pytest

from pathlib import Path
from ymlstash import YmlStash
from dataclasses import dataclass
from typing import ClassVar


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
    stash.save(yuval, "foo")
    assert stash.list_all_keys() == ["foo"]
    obj = stash.load("foo")
    assert obj == yuval
    stash.drop()
    assert stash.list_all_keys() == []


def test_key_field():
    @dataclass
    class Rat:
        key: ClassVar[str] = "name"

    with pytest.raises(Exception):
        YmlStash(Rat, ".")

    @dataclass
    class Dog:
        name: str
        key: ClassVar[str] = "name"

    stash = YmlStash(Dog, "/tmp/")
    terra = Dog(name="terra")
    stash.save(terra)
    assert stash.list_all_keys() == ["terra"]

    terra = Dog(name="terra")
    stash.save(terra, key="dupe")  # override key
    assert stash.list_all_keys() == ["terra", "dupe"]

    stash.drop()

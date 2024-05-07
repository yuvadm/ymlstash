import pytest

from pathlib import Path
from ymlstash import YmlStash
from dataclasses import dataclass
from typing import ClassVar

TEST_STASH_PATH = "/tmp"


@dataclass
class User:
    name: str
    age: int


def test_stash_path():
    stash = YmlStash(User, ".")
    assert stash.path == Path(".")
    stash = YmlStash(User, Path("."))
    assert stash.path == Path(".")


def test_invalid_path():
    with pytest.raises(Exception):
        YmlStash(User, "/tmp/does/not/exist")


def test_stash():
    stash = YmlStash(User, TEST_STASH_PATH)
    yuval = User(name="yuval", age=42)
    stash.save(yuval, "foo")
    assert stash.list_keys() == ["foo"]
    obj = stash.load("foo")
    assert obj == yuval
    stash.drop()
    assert stash.list_keys() == []


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

    stash = YmlStash(Dog, TEST_STASH_PATH)
    terra = Dog(name="terra")
    stash.save(terra)
    assert stash.list_keys() == ["terra"]

    terra = Dog(name="terra")
    stash.save(terra, key="dupe")  # override key
    assert stash.list_keys() == ["terra", "dupe"]

    stash.drop()

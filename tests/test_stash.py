import pytest

from pathlib import Path
from ymlstash import YmlStash
from dataclasses import dataclass
from typing import ClassVar, Optional

TEST_STASH_PATH = Path("/tmp")


@dataclass
class User:
    name: str
    age: int


def test_stash_path():
    stash = YmlStash(User, ".")
    assert stash.path == Path(".")
    stash = YmlStash(User, Path("."))
    assert stash.path == Path(".")


def test_invalid():
    with pytest.raises(Exception):
        YmlStash(User, "/tmp/does/not/exist")
    with pytest.raises(Exception) as e:
        YmlStash(object, ".")
    assert "is not a dataclass" in e.value.args[0]


def test_stash():
    stash = YmlStash(User, TEST_STASH_PATH)

    yuval = User(name="yuval", age=42)
    stash.save(yuval, "foo")
    assert stash.exists("foo")
    assert not stash.exists("goo")
    assert stash.list_keys() == ["foo"]

    obj = stash.load("foo")
    assert obj == yuval

    goo = User(name="goo", age=10)
    stash.save(goo, "goo")
    assert stash.list_keys() == ["foo", "goo"]

    stash.delete("foo")
    assert stash.list_keys() == ["goo"]

    with pytest.raises(Exception):
        stash.delete("foo")

    stash.drop()
    assert stash.list_keys() == []


def test_key_field():
    @dataclass
    class Rat:
        key: ClassVar[str] = "foo"

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


def test_dump_order():
    @dataclass
    class Order:
        o: int
        r: int
        d: int
        e: int
        a: int
        z: int
        key: ClassVar[str] = "o"

    stash = YmlStash(Order, TEST_STASH_PATH)
    order = Order(1, 2, 3, 4, 5, 6)
    stash.save(order)

    with open(TEST_STASH_PATH / "1.yml", "r") as f:
        lines = f.readlines()
        keys = "".join([line[0] for line in lines])
        assert keys == "ordeaz"

    stash.drop()


def test_null_values():
    @dataclass
    class Nullable:
        name: str
        nullval: Optional[str] = None
        key: ClassVar[str] = "name"

    stash = YmlStash(Nullable, TEST_STASH_PATH, filter_none=True)
    goo = Nullable("goo")
    stash.save(goo)

    with open(TEST_STASH_PATH / "goo.yml", "r") as f:
        lines = f.readlines()
        for line in lines:
            assert "nullval" not in line

    stash.drop()

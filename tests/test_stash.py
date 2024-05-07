from pathlib import Path
from ymlstash import YmlStash


def test_stash_path():
    stash = YmlStash("foo")
    assert stash.path == Path("foo")
    stash = YmlStash(Path("foo"))
    assert stash.path == Path("foo")

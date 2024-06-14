import pytest
from mainframe_paxo import registry
from mainframe_paxo.registry import Key


@pytest.fixture
def root():
    k = registry.Key.current_user("Software\\gumbotron\\test")
    k.delete(tree=True)
    k.create()
    with k:
        yield k
    # k.delete(tree=True)


def test_fresh_key(root):
    with root.create("dude") as k:
        assert k.exists()
        with pytest.raises(KeyError):
            k[""]
        k[""] = "hello"
        assert k[""] == "hello"


def test_as_dict(root):
    with root.create("dude") as k:
        k["a"] = "hello"
        k["b"] = "world"
        assert k.as_dict() == {"values": {"a": "hello", "b": "world"}, "keys": {}}
        with k.create("dub", "rub") as k2:
            k2["c"] = "goodbye"
            assert k.as_dict() == {
                "values": {"a": "hello", "b": "world"},
                "keys": {
                    "dub": {
                        "values": {},
                        "keys": {"rub": {"values": {"c": "goodbye"}, "keys": {}}},
                    }
                },
            }


def test_from_dict(root):
    pattern = {
        "values": {"a": "hello", "b": "world"},
        "keys": {
            "dub": {
                "values": {},
                "keys": {"rub": {"values": {"c": "goodbye"}, "keys": {}}},
            }
        },
    }
    with root.create("dude") as k:
        k.from_dict(pattern)

    with root.open("dude") as k:
        assert k.as_dict() == pattern


def test_from_dict_remove(root):
    pattern = {
        "values": {"a": "hello", "b": "world"},
        "keys": {
            "dub": {
                "values": {"bozo": "clown"},
                "keys": {
                    "rub": {"values": {"c": "goodbye"}, "keys": {}},
                    "tub": {"values": {"d": "goodbye"}, "keys": {}},
                },
            }
        },
    }
    with root.create("dude") as k:
        k.from_dict(pattern)
        assert k.as_dict() == pattern
        del pattern["keys"]["dub"]["keys"]["tub"]
        del pattern["keys"]["dub"]["values"]["bozo"]
        k.from_dict(pattern, remove=True)
        assert k.as_dict() == pattern


def test_roots():
    assert Key.classes_root().exists()


def test_value_types(root):
    root["a"] = 1
    assert root["a"] == 1

    root["a"] = "buumgo"
    assert root["a"] == "buumgo"

    root["a"] = b"foo"
    assert root["a"] == b"foo"

    root["a"] = None
    assert root["a"] is None

    root["a"] = b""
    assert root["a"] == b""


def test_open_from_root():
    """check that we can open a key from a root"""
    root = Key.local_machine("Software\\Classes", "gumbotron")

    with pytest.raises(ValueError):
        with root(".uproject"):
            pass

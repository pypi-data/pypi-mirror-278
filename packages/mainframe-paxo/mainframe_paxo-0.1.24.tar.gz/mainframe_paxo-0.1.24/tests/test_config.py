from mainframe_paxo.uebase.config_cache import UEConfigParser

config1 = """
[/Script/Engine.PlayerInput]
Bindings=(Name="Q",Command="Foo")
.Bindings=(Name="Q",Command="Bar")
.Bindings=(Name="Q",Command="Foo")
dude=foo
bob = hope
  eternal
"""

config2 = """
[/Script/Engine.PlayerInput]
+Bindings=(Name="Q",Command="Foo")
.Bindings=(Name="Q",Command="Bar")
+Bindings=(Name="Q",Command="Foo")
dude=foo
bob = hope
  eternal
"""


def test_ue_config_parser():
    parser = UEConfigParser()
    parser.read_string(config1)
    assert list(parser["/Script/Engine.PlayerInput"]["Bindings"]) == [
        '(Name="Q",Command="Foo")',
        '(Name="Q",Command="Bar")',
        '(Name="Q",Command="Foo")',
    ]
    assert parser["/Script/Engine.PlayerInput"]["dude"] == "foo"
    assert parser["/Script/Engine.PlayerInput"]["bob"] == "hope\neternal"


def test_ue_config_parser2():
    parser = UEConfigParser()
    parser.read_string(config2)
    assert list(parser["/Script/Engine.PlayerInput"]["Bindings"]) == [
        '(Name="Q",Command="Foo")',
        '(Name="Q",Command="Bar")',
    ]
    assert parser["/Script/Engine.PlayerInput"]["dude"] == "foo"
    assert parser["/Script/Engine.PlayerInput"]["bob"] == "hope\neternal"


def test_ue_config_parser3():
    parser = UEConfigParser()
    parser.read_string(config1)
    print("------------")
    parser.read_string(config2)
    assert list(parser["/Script/Engine.PlayerInput"]["Bindings"]) == [
        '(Name="Q",Command="Foo")',
        '(Name="Q",Command="Bar")',
        '(Name="Q",Command="Foo")',
        '(Name="Q",Command="Bar")',
    ]
    assert parser["/Script/Engine.PlayerInput"]["dude"] == "foo"
    assert parser["/Script/Engine.PlayerInput"]["bob"] == "hope\neternal"

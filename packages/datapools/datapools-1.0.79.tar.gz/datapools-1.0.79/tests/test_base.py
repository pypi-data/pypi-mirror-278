from datapools.worker.plugins.base_plugin import BasePlugin, BaseTag
from datapools.worker.plugins.ftp import FTPPlugin


def test_tag_parsing():
    t = BasePlugin.parse_tag_in_str("https://openlicense.ai/asd")
    assert isinstance(t, BaseTag)
    assert str(t) == "asd"
    assert t.is_keepout() is False

    t = BasePlugin.parse_tag_in_str("https://openlicense.ai/t/asd")
    assert isinstance(t, BaseTag)
    assert str(t) == "asd"
    assert t.is_keepout() is False

    t = BasePlugin.parse_tag_in_str("https://openlicense.ai/n/asd")
    assert isinstance(t, BaseTag)
    assert str(t) == "asd"
    assert t.is_keepout() is True

    t = BasePlugin.parse_tag_in_str("https://openlicense.ai/xxx/asd")
    assert t is None


def test_ftp_link_parsing():
    (user, passwd, host, port) = FTPPlugin.parse_ftp_url("ftp://user:password@host:21")
    assert user == "user"
    assert passwd == "password"
    assert host == "host"
    assert port == 21

    (user, passwd, host, port) = FTPPlugin.parse_ftp_url("ftp://host:21")
    assert user == "anonymous"
    assert passwd == ""
    assert host == "host"
    assert port == 21

    (user, passwd, host, port) = FTPPlugin.parse_ftp_url("ftp://user@host:22")
    assert user == "user"
    assert passwd == ""
    assert host == "host"
    assert port == 22

    (user, passwd, host, port) = FTPPlugin.parse_ftp_url("ftp://user@host")
    assert user == "user"
    assert passwd == ""
    assert host == "host"
    assert port == 21

    (user, passwd, host, port) = FTPPlugin.parse_ftp_url("ftp://host")
    assert user == "anonymous"
    assert passwd == ""
    assert host == "host"
    assert port == 21

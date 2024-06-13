from open_api_framework.conf.utils import config


def test_empty_list_as_default():
    value = config("SOME_TEST_ENVVAR", split=True, default=[])

    assert value == []


def test_non_empty_list_as_default():
    value = config("SOME_TEST_ENVVAR", split=True, default=["foo"])

    assert value == ["foo"]

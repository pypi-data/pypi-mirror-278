from oas_mini.swagg.flags import Flag


def test_get_usage():
    flag_mock = Flag("-a", "--abc")
    usage = flag_mock.get_usage()
    assert usage == "[--abc, -a]"


def test_is_in():
    flag_mock = Flag("-a", "--abc")
    assert flag_mock.is_in(["-a"])

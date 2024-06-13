import autowork_cli.log.log_cmd as log


def test_enable_debug():
    log.enable_debug()
    assert log.is_debug()


def test_disable_debug():
    log.disable_debug()
    assert not log.is_debug()

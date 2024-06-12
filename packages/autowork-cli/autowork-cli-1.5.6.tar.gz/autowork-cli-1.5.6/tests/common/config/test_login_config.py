from pathlib import Path

from autowork_cli.common.config.LoginConfig import LoginConfig

DIR = str(Path(__file__).parents[0])


def test_read():
    config = LoginConfig(DIR + '/test1.ini')
    assert config.GLOBAL_CONFIG.ENV == "DEV"
    assert config.GLOBAL_CONFIG.DEV_APPS == "app1,app2"
    assert config.DEV.API_KEY == "DEV1"
    assert config.BETA.API_KEY == "BETA2"


def test_write():
    try:
        config = LoginConfig(DIR + '/test1.ini')
        config.GLOBAL_CONFIG.ENV = "BETA"
        config.GLOBAL_CONFIG.DEV_APPS = "app3,app4"
        config.BETA.API_KEY = "BETA3"
        config.save(DIR + '/test1_write.ini')

        config = LoginConfig(DIR + '/test1_write.ini')
        assert config.GLOBAL_CONFIG.ENV == "BETA"
        assert config.GLOBAL_CONFIG.DEV_APPS == "app3,app4"
        assert config.BETA.API_KEY == "BETA3"
    finally:
        Path(DIR + '/test1_write.ini').unlink()


def test_home_path():
    import os
    h1 = str(Path.home())  # os.environ['HOME']
    # h2 = os.path.expandvars('$HOME')
    h3 = os.path.expanduser('~')
    print([h1, h3])
    assert h1 == h3

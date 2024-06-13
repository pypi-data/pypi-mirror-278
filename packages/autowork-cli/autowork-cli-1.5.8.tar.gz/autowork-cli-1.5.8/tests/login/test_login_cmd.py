import shutil
import unittest
from pathlib import Path

import pytest

from autowork_cli.common.config.LoginConfig import LoginConfig, get_config_file_path, set_config_file_path
from autowork_cli.login.login_cmd import LoginCommand

DIR = str(Path(__file__).parents[0])


@pytest.fixture(scope="module", autouse=True)
def my_fixture():
    print('记录默认配置')
    old_config_path = get_config_file_path()
    yield
    print('恢复默认配置')
    set_config_file_path(old_config_path)


def test_login():
    init_path = DIR + '/a/b/c/login_none.ini'
    set_config_file_path(init_path)
    try:
        config = LoginConfig()
        config.set_env("BETA")
        config.set_dev_apps("app1,app2")
        config.set_api_key("BETA4")
        config.save()

        config = LoginConfig()
        assert config.get_env() == "BETA"
        assert config.get_api_key() == "BETA4"
        assert config.get_dev_apps() == "app1,app2"
    finally:
        shutil.rmtree(DIR + "/a", ignore_errors=True)


@unittest.skip("依赖本地配置APIKEY，暂时不测试")
def test_hello():
    cmd = LoginCommand()
    cmd.hello()

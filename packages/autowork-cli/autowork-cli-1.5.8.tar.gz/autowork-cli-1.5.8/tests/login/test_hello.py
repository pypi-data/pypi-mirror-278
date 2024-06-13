import unittest

import pytest
from typer.testing import CliRunner

from autowork_cli.__main__ import app

runner = CliRunner()


@unittest.skip("需要交互输入")
def test_login_cmd():
    result = runner.invoke(app, ["login"])
    assert result.exit_code == 1
    print(result.stdout)
    assert "登录 Autowork..." in result.stdout

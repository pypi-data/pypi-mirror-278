PYPROJECT_TEMPLATE = """
[tool.poetry]
name = "{project_id}"
version = "0.1.0"
description = ""
authors = ["user <user@yunzhangfang.com>"]
packages = [{ include = "{project_id}" }]

[tool.poetry.dependencies]
python = "^3.11,<3.12"
sandbox-func = {version = "^0.4.1", source = "private"}

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.1"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.pytest.ini_options]
log_cli = true
log_cli_level = "INFO"
log_cli_format = "%(asctime)s [%(levelname)5s] %(name)s:%(filename)s:%(lineno)s - %(message)s"
log_cli_date_format = "%Y-%m-%d %H:%M:%S"

[[tool.poetry.source]]
name = "custom"
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true

[[tool.poetry.source]]
name = "private"
url = "http://172.23.50.109:18083/repository/pypi-group/simple"
"""
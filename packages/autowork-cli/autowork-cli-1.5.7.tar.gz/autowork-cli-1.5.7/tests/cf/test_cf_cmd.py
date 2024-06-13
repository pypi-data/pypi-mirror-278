import os
import shutil
import unittest
from pathlib import Path

import autowork_cli.cf.cf_cmd as cf


@unittest.skip('测试一下')
def testInit():
    curr_dir = Path(__file__).resolve().parent.parent
    demo_dir = curr_dir.joinpath('demo')
    tests_dir = curr_dir.joinpath('tests')
    pyproject_file = curr_dir.joinpath('pyproject.toml')
    sandbox_function_json = curr_dir.joinpath('sandbox_function.json')
    sandbox_boot = curr_dir.joinpath('sandbox_boot')

    cf.init(project_id='demo', app_id='demo')
    assert demo_dir.exists()
    assert tests_dir.exists()
    assert pyproject_file.exists()
    assert sandbox_function_json.exists()
    assert sandbox_boot.exists()

    clear(demo_dir, tests_dir, pyproject_file, sandbox_function_json, sandbox_boot)


def clear(project_dir: Path, tests_dir: Path, pyproject: Path, sandbox_function_json: Path, sandbox_boot: Path):
    if project_dir.exists():
        shutil.rmtree(project_dir)
    if tests_dir.exists():
        shutil.rmtree(tests_dir)
    if pyproject.exists():
        os.remove(pyproject)
    if sandbox_function_json.exists():
        os.remove(sandbox_function_json)
    if sandbox_boot.exists():
        shutil.rmtree(sandbox_boot)

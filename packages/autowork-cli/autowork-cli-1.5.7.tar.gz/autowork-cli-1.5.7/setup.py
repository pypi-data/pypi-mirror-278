from setuptools import setup, find_packages

DEV_API_KEY = "ALPHA-d8e7634b2f7f4ae5a23896b93a23006f046fa00ff5cc485aad64ec8c05866e73"

setup(
    name="autowork-cli",
    version="1.5.7",
    description="沙盒函数命令行工具",
    packages=find_packages(),
    python_requires='>=3.11',
    entry_points={
      'console_scripts': ['autowork=autowork_cli.__main__:run'],
    },
)

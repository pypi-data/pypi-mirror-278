from setuptools import setup, find_packages

setup(
    name="autowork-cli",
    version="1.5.6",
    description="沙盒函数命令行工具",
    packages=find_packages(),
    python_requires='>=3.11',
    entry_points={
      'console_scripts': ['autowork=autowork_cli.__main__:run'],
    },
)

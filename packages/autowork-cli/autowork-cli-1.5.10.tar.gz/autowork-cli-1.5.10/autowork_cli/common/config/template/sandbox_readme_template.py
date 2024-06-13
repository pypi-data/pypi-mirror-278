SANDBOX_README_TEMPLATE = """# 沙盒函数
> 自由编写代码实现业务逻辑

## 环境配置

### 安装 Python

确保的你的机器拥有 python 3.11 环境。

### 安装 Poetry

项目使用 poetry 进行依赖管理，执行以下命令安装 poetry。

```
>> python -m pip install --upgrade pip
>> pip install poetry
```

### 安装依赖

切换到当前项目路径下，执行如下命令安装项目依赖 。

```
>> poetry install -v
```

### PyCharm 配置

由于 PyCharm 无法自动识别 Poetry 创建的虚拟环境，所以要手动指定。

执行如下命令查看当期的虚拟环境信息，可以获得虚拟环境的 Python 解释器可执行文件（Executable）的路径。

```
>> poetry env info
```

Settings -> Project -> Python Interpreter，将该解释器添加到 PyCharm，并设置成项目解释器。

## 项目运行

### 启动

通过sandbox_start.py文件启动项目。

### 执行函数

通过CLI命令(autowork sidecar start)启动边车，即可进行本地运行调试。
"""
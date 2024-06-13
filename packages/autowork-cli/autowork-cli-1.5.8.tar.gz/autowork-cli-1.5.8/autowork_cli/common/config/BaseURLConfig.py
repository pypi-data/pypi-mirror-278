from autowork_cli.common.config.LoginConfig import DefaultLoginConfig


class BaseURLConfig:
    product_name: str
    api: str
    domain: dict

    @classmethod
    def get_api_base_url(cls, env: str):
        env = env.upper()
        if env == 'LOCAL':
            return cls.domain[env]
        else:
            return cls.domain[env] + cls.api

    @classmethod
    def get_domain_url(cls, env):
        return cls.domain[env]

    @classmethod
    def get_env_list(cls):
        return list(cls.domain.keys())


class CybotronURLConfig(BaseURLConfig):
    product_name = 'CYBOTRON'
    api = '/cybotron-client'
    domain = {
        "LOCAL": "http://127.0.0.1:8080",
        "DEV": "http://cybotron-dev.yunzhangfang.com",
        "ALPHA": "http://cybotron-alpha.yunzhangfang.com",
        "BETA": "http://cybotron-beta.yunzhangfang.com",
        "TEST": "http://cybotron-test.yunzhangfang.com",
        "PROD": "http://cybotron.yunzhangfang.com",
    }


class FastAppURLConfig(BaseURLConfig):
    product_name = 'FASTAPP'
    api = '/fast_app'
    domain = {
        "BETA": "https://fastapp-beta.yunzhangfang.com",
        "PROD": "https://fastapp.yunzhangfang.com",
    }


def get_url_config(product_name: str) -> any:
    if not product_name:
        return []
    return [_cls for _cls in BaseURLConfig.__subclasses__() if _cls.product_name == product_name][0]


DefaultURLConfig = get_url_config(DefaultLoginConfig.get_product())

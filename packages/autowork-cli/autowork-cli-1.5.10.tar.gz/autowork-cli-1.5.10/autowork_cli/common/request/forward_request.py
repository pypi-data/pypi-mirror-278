import os
import logging

from autowork_cli.common.config.PublicConfig import OTHER
from autowork_cli.common.lang.async_requests import AsyncRequests
from autowork_cli.common.config.BaseURLConfig import DefaultURLConfig
from autowork_cli.common.config.LoginConfig import DefaultLoginConfig

logger = logging.getLogger(__name__)
MASTER_KEY = os.getenv('api_key')


class ForwardRequest:
    api_key: dict[str: str] = {}  # 缓存key
    client = AsyncRequests(
        base_url=DefaultLoginConfig.get_other_url() if DefaultLoginConfig.get_env() == OTHER else DefaultURLConfig.get_api_base_url(
            DefaultLoginConfig.get_env()))

    @staticmethod
    async def __get_new_headers(headers) -> dict:
        """
        根据原有请求头生成新的请求头
        :param headers: 原始请求头
        :return:
        """
        tenant_id = headers['X-TENANT-ID']
        config_tenant_id = DefaultLoginConfig.get_tenant_id()
        if config_tenant_id != tenant_id:
            raise Exception('当前请求租户ID与本地配置文件不符，请检查')
        new_headers = {
            'X-TENANT-ID': tenant_id,
            'X-API-KEY': DefaultLoginConfig.get_api_key(),
            'content-type': headers['content-type'],
            'content-length': headers['content-length']
        }
        return new_headers

    @classmethod
    async def send(cls, request):
        """
        转发业务请求
        :param request: 请求对象
        :return:
        """
        try:
            method, url = request.headers['original-request'].split('__')
            body = await request.body()
            new_headers = await cls.__get_new_headers(request.headers)
            req = cls.client.build_request(method=method, url=url, data=body, headers=new_headers)
            logger.info('转发业务请求：tenant_id({}), method({}), url({})'.format(
                request.headers['X-TENANT-ID'], method, cls.client.base_url + url))
            response = await cls.client.send(req)
            res = response.json()
            return res
        except Exception as e:
            logger.error("转发业务请求异常：{}".format(e))
            return {'success': False, "message": "转发业务请求异常: {}".format(e)}

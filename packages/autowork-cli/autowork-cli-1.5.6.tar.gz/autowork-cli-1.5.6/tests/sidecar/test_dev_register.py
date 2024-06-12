import pytest

from autowork_cli.sidecar.dev_register import DevRouterRegister


@pytest.mark.skip("开发者路由暂时不上报，api-key便捷提供后放开")
@pytest.mark.asyncio
async def test_register_develop_router():
    result = DevRouterRegister.register()
    assert result
    query_result = await DevRouterRegister.query()
    assert query_result
    await DevRouterRegister.stop()
    query_result = await DevRouterRegister.query()
    assert query_result is None

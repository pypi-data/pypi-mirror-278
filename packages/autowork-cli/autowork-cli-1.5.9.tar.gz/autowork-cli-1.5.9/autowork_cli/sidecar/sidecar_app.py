import os

from autowork_cli.common.log.AwLogger import AwLogger, Log, LogRecord
from fastapi import Request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from autowork_cli.common.lang import logger_setting
from autowork_cli.common.lang.async_requests import AsyncRequests
from autowork_cli.sidecar.dev_register import DevRouterRegister
from autowork_cli.sidecar.dev_websocket import DevWebSocketStart
from autowork_cli.sidecar.sidecar_mgr import SidecarManager
from autowork_cli.common.request.forward_request import ForwardRequest

logger_setting.init()
logger = AwLogger.getLogger(__name__)

sidecar_mgr = SidecarManager()
app = FastAPI(title="Autowork CLI Sidecar")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def dev_router_startup():
    DevWebSocketStart.start()


@app.on_event("shutdown")
async def dev_router_shutdown():
    pass


@app.get("/health")
async def health():
    return {
        "pid": os.getpid()
    }


@app.post("/forward-request")
async def forward_request(request: Request):
    """
    转发业务请求
    :param request:
    :return:
    """
    res = await ForwardRequest.send(request)
    return res


@app.post("/sandbox/call/{app_id}/{func_id}")
async def call_sandbox_func(app_id: str, func_id: str, req: Request, debug: bool = False):
    global trace_id
    try:
        app_port = sidecar_mgr.app_port
        client = AsyncRequests(f"http://localhost:{str(app_port)}")
        data = await req.json()

        trace_id = data['traceId']
        cybotron_access_info = Log(
            trace_id=trace_id,
            app_id=app_id,
            func_id=func_id,
        )
        AwLogger.cybotron_access_info[trace_id] = cybotron_access_info
        logger.info(f'本地边车服务转发赛博坦平台请求，应用编号：{app_id}, 函数编号：{func_id}, 参数：{data}', LogRecord(trace_id=trace_id))

        timeout = 30 * 60 if debug else 10
        resp = await client.request(f"/sandbox/call/{app_id}/{func_id}/local", data, timeout)
        return resp.json()
    except BaseException as e:
        logger.info(f'本地边车服务转发赛博坦平台请求报错，应用编号：{app_id}, 函数编号：{func_id}, 参数：{data}, 报错信息：{e}', LogRecord(trace_id=trace_id))
        return {"message": str(e), "success": False}


async def exec_sandbox_func(app_id: str, func_id: str, data):
    global trace_id
    try:
        app_port = sidecar_mgr.app_port
        client = AsyncRequests(f"http://localhost:{str(app_port)}")


        trace_id = data['traceId']
        cybotron_access_info = Log(
            trace_id=trace_id,
            app_id=app_id,
            func_id=func_id,
        )
        AwLogger.cybotron_access_info[trace_id] = cybotron_access_info
        logger.info(f'本地边车服务转发赛博坦平台请求，应用编号：{app_id}, 函数编号：{func_id}, 参数：{data}', LogRecord(trace_id=trace_id))

        resp = await client.request(f"/sandbox/call", data, timeout=3600)
        return resp.json()
    except BaseException as e:
        logger.info(f'本地边车服务转发赛博坦平台请求报错，应用编号：{app_id}, 函数编号：{func_id}, 参数：{data}, 报错信息：{e}', LogRecord(trace_id=trace_id))
        return {"error": str(e), "success": False}

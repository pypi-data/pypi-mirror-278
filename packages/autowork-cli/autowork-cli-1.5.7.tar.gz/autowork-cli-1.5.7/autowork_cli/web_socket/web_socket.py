# -*- coding: utf-8 -*-
import asyncio
import logging
import os
import threading
from typing import Optional
import websocket
import json
import time
from websocket import WebSocketApp
from autowork_cli.common.config.BaseURLConfig import DefaultURLConfig
from autowork_cli.common.config.LoginConfig import DefaultLoginConfig
from autowork_cli.common.config.PublicConfig import OTHER
from autowork_cli.common.local.clientinfo import ClientInfo
from autowork_cli.sidecar.dev_register import DevRouterRegister
from autowork_cli.sidecar.sidecar_app import exec_sandbox_func
from autowork_cli.web_socket.model import WebSocketEvent, parse_body

logger = logging.getLogger(__name__)

try:
    import thread
except ImportError:
    import _thread as thread
env = DefaultLoginConfig.get_env()
DOMAIN_URL = DefaultLoginConfig.get_other_domain_url() if env == OTHER else DefaultURLConfig.get_domain_url(env)
WS_URI = f"ws://{DOMAIN_URL.split('://')[-1]}/ws/v1/devRoute"
# WS_URI = "ws://127.0.0.1:8443/v1"

stop_register = False
reconnect_count = 0
ws: Optional[WebSocketApp] = None

def register_router():
    while True:
        if stop_register:
            return
        api_dev_router_do = {
            'devApps': DefaultLoginConfig.get_dev_apps().split(','),
            'serviceId': 'SandboxFunction',
            'address': ClientInfo.get_ip(),
            'port': 8081,
            'computerName': DevRouterRegister.query_computer_name()
        }
        send_message = json.dumps({
            'event': WebSocketEvent.register,
            'content': json.dumps(api_dev_router_do),
        })
        ws.send(send_message)
        logger.info("注册开发者路由")
        time.sleep(5)


def event_register_success():
    global stop_register, reconnect_count
    stop_register = True
    reconnect_count = 0
    logger.info("开发者路由注册成功")


async def event_call_func(message_data):
    message_data = json.loads(message_data['content'])
    websocket_req = parse_body(message_data)
    app_id = websocket_req.appId
    func_id = websocket_req.funcId
    class_file = websocket_req.metadata.classFile
    method_name = websocket_req.metadata.methodName
    data = websocket_req.model_dump()
    data.update({"class_file": class_file, "method_name": method_name,
                 "request_id": websocket_req.requestId, "tenant_id": websocket_req.tenantId})
    res = await exec_sandbox_func(app_id, func_id, data)
    result = {
        'metadata': websocket_req.metadata.model_dump(),
        'result': res,
        "requestId": websocket_req.requestId,
        "traceId": websocket_req.traceId,
    }
    send_message = json.dumps({
        'event': WebSocketEvent.call_func_resp,
        'content': json.dumps(result)
    })
    ws.send(send_message)
    logger.info(f"{WebSocketEvent.call_func_resp} of message: {send_message}")
    return res


def on_message(ws, message):
    logger.info("Received message from server: " + message)
    message_data = json.loads(message)
    event = message_data.get('event')
    if event == WebSocketEvent.connect_success:
        thread.start_new_thread(register_router, ())
    elif event == WebSocketEvent.register_success:
        event_register_success()
    elif event == WebSocketEvent.call_func:
        t = threading.Thread(
            target=asyncio.run,
            args=(event_call_func(message_data),)
        )
        t.start()


def on_error(ws, error):
    logger.exception(error)


def on_open(ws):
    global reconnect_count
    logger.info("Connected to server")



def on_close(ws, close_status_code, close_reason):
    logger.info("### websock closed ###")
    logger.info(f"on_close, {close_status_code}, {close_reason}")
    if close_status_code:
        reconnect()
    else:
        os._exit(0)  # noqa


def reconnect():
    global reconnect_count
    time.sleep(5)
    if reconnect_count > 5:
        os._exit(0)  # noqa
        return
    reconnect_count += 1
    logger.info(f'重连中, 第{reconnect_count}次重连')
    start_websocket()

def get_headers():
    api_key = DefaultLoginConfig.get_api_key()
    tenant_id = DefaultLoginConfig.get_tenant_id()
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': api_key,
        'X-TENANT-ID': tenant_id
    }
    return headers


def start_websocket():
    global ws
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(WS_URI,
                                header=get_headers(),
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close
                                )
    ws.run_forever()


if __name__ == '__main__':
    start_websocket()

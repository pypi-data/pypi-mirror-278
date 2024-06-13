# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel


class WebSocketEvent:
    connect_success = 'connect_success'
    register = 'register'
    register_success = 'register_success'
    call_func = "call_func"
    call_func_resp = "call_func_resp"


class Metadata(BaseModel):
    repoCode: str
    repoVersionCode: str
    classFile: str
    methodName: str

class WebSocketRequest(BaseModel):
    metadata: Metadata
    input: dict = {}
    tenantId: Optional[str]
    requestId: Optional[str]
    traceId: str
    appId: str
    funcId: str
    tenantId: str

def parse_body(body: dict) -> WebSocketRequest:
    """
    解析请求体，拆分input参数
    :param body: 请求体
    :return:
    """
    input_params = {}
    new_body = {}
    fields = WebSocketRequest.model_fields
    for k, v in body.items():
        if k in fields:
            new_body[k] = v
        else:
            input_params[k] = v
    if not new_body.get('input') and input_params:
        new_body.update({"input": input_params})
    websocket_req = WebSocketRequest(**new_body)
    return websocket_req

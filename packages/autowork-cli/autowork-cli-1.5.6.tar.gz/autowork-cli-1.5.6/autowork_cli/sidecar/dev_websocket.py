# -*- coding: utf-8 -*-
import logging
import threading


logger = logging.getLogger(__name__)


class DevWebSocketStart:

    @classmethod
    def start(cls):
        from autowork_cli.web_socket.web_socket import start_websocket
        upload_thread = threading.Thread(target=start_websocket, daemon=True, name="启动WebSocket")
        upload_thread.start()

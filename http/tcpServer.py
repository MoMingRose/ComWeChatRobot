# -*- coding: utf-8 -*-
# tcpServer.py created by MoMingLog on 25/3/2024.
"""
【作者】MoMingLog
【创建时间】2024-03-25
【功能描述】
"""
import json
import pprint
import re
import socketserver
import threading


class ReceiveMsgSocketServer(socketserver.BaseRequestHandler):
    url_compile = re.compile(r"<url.*?(https.*?)\].*?url", re.S)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self):
        conn = self.request
        while True:
            try:
                ptr_data = b""
                while True:
                    data = conn.recv(1024)
                    ptr_data += data
                    if len(data) == 0 or data[-1] == 0xA:
                        break
                json_msg = ptr_data.decode("utf-8")
                msg = json.loads(ptr_data.decode('utf-8'))
                if "订单状态提醒" in json_msg:
                    ReceiveMsgSocketServer.handle_article(msg)
                else:
                    ReceiveMsgSocketServer.msg_callback(msg)
            except OSError:
                break
            except json.JSONDecodeError:
                pass
            conn.sendall("200 OK".encode())
        conn.close()

    @staticmethod
    def msg_callback(msg):
        pprint.pprint(msg)

    @staticmethod
    def handle_article(msg):
        html = msg.get("message")
        if html is not None:
            url = ReceiveMsgSocketServer.url_compile.search(html)
            if url:
                print(f"========={url}")
                # post_wechat_http_api(APIS.WECHAT_BROWSER_OPEN_WITH_URL, port=8000, data={"url": url.group(1)})


def start_socket_server(
        port: int = 10808,
        request_handler=ReceiveMsgSocketServer,
        main_thread: bool = True
) -> int or None:
    ip_port = ("127.0.0.1", port)
    try:
        s = socketserver.ThreadingTCPServer(ip_port, request_handler)
        if main_thread:
            s.serve_forever()
        else:
            socket_server = threading.Thread(target=s.serve_forever)
            socket_server.setDaemon(True)
            socket_server.start()
            return socket_server.ident
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    return None


if __name__ == '__main__':
    start_socket_server()

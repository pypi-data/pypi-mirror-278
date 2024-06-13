import urllib.parse
from http.client import HTTPConnection, HTTPResponse
from json import dumps, loads
from logging import Logger

from requests import Session
from urllib3.filepost import choose_boundary

from lljz_tools import logger
from lljz_tools.color import Color
from lljz_tools.decorators import thread_lock, debug


class HTTPClient(Session):

    def __init__(self, base_url: str = '', *, timeout=120, debug: bool | Logger = False):
        super().__init__()
        self._base_url = base_url.rstrip('/')
        self._timeout = timeout
        self.debug = bool(debug)
        self._logger = debug if isinstance(debug, Logger) else logger

    def request(
            self,
            method,
            url,
            params=None,
            data=None,
            headers=None,
            cookies=None,
            files=None,
            auth=None,
            timeout=None,
            allow_redirects=True,
            proxies=None,
            hooks=None,
            stream=None,
            verify=False,
            cert=None,
            json=None,
    ):
        if not url.startswith('http://') and not url.startswith('https://'):
            url = self._base_url + url
        if self.debug:
            method = method.upper()
            method_color = {
                'POST': Color.yellow, 'GET': Color.green, 'DELETE': Color.red, 'PUT': Color.magenta
            }.get(method, Color.cyan)
            self._logger.info(f'{method_color(method)} - {url}', stacklevel=5)
        if self.debug and params:
            self._logger.info(f'params - {params}', stacklevel=5)
        if self.debug and json:
            try:
                json_data = dumps(json, ensure_ascii=False)
                self._logger.info(f'Payload - {json_data}', stacklevel=5)
            except TypeError as e:
                self._logger.error(f'json dumps error: {e}', stacklevel=5)
        if self.debug and data:
            self._logger.info(f'Form data - {data}', stacklevel=5)

        return super().request(
            method, url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
        )


class FastResponse:

    def __init__(self, response: HTTPResponse):
        self._response = response
        self.status_code = response.status
        self.content = response.read()
        self.text = self.content.decode('utf-8')
        self.headers = response.headers
        self._json = None

    def json(self):
        if not self._json:
            self._json = loads(self.text)
        return self._json

    def __repr__(self):
        return f'<FastResponse [{self.status_code}]>'

    def __bool__(self):
        return self.status_code == 200

    def __str__(self):
        return f'<FastResponse [{self.status_code}]>'


class FastHTTPClient:

    def __init__(self, base_url: str = '', *, timeout=120, debug: bool | Logger = False):
        if base_url.startswith('https://'):
            raise ValueError('FastHTTPClient 不支持https协议')
        self._base_url = urllib.parse.urlparse(base_url)
        self._timeout = timeout
        self.debug = debug
        self._connections: list[list[HTTPConnection | bool]] = []
        self._closed = False
        self.headers = {}
        self.debug = bool(debug)
        self._logger = debug if isinstance(debug, Logger) else logger

    @thread_lock
    def __get_connection(self) -> tuple[int, HTTPConnection]:
        if self._closed:
            raise ValueError("FastHTTPClient 已关闭")
        for index, (connection, status) in enumerate(self._connections):
            if not status:
                self._connections[index][1] = True
                return index, connection
        else:
            self._connections.append([HTTPConnection(self._base_url.netloc, timeout=self._timeout), True])
            return len(self._connections) - 1, self._connections[-1][0]

    def set_token(self, token: str, key='Authorization'):
        if len(token.split(' ')) == 1:
            token = f"Bearer {token}"
        self.headers[key] = token

    @staticmethod
    def _encode_data_to_form_data(data):
        """将dict转换为multipart/form-data"""
        body = b''
        boundary = f'----{choose_boundary()}'
        content_type = f'multipart/form-data; boundary={boundary}'  # noqa
        for key, value in data.items():
            value = "" if value is None else str(value)
            body += f'--{boundary}\r\n'.encode('utf-8')
            body += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode('utf-8')  # noqa
            body += f'{value}\r\n'.encode('utf-8')
        body += f'--{boundary}--'.encode('utf-8')
        return body, content_type

    def request(self, method, url: str, *, params=None, data=None, json=None, headers=None, **kwargs):
        if url.startswith('http://') or url.startswith('https://'):
            raise ValueError('URL不允许重新指定网络地址')
        if data and json:
            raise ValueError('data和json不能同时存在')
        if params:
            url = f'{url}?{urllib.parse.urlencode(params)}'
        if self.debug:
            method = method.upper()
            method_color = {
                'POST': Color.yellow, 'GET': Color.green, 'DELETE': Color.red, 'PUT': Color.magenta
            }.get(method, Color.cyan)
            self._logger.info(
                f'{method_color(method)} - {self._base_url.scheme}://{self._base_url.netloc}{url}', stacklevel=5
            )
        body = None
        if not headers:
            headers = {}
        if json:
            body = dumps(json, ensure_ascii=True)
            if self.debug:
                self._logger.info(f'Payload - {dumps(json, ensure_ascii=False)}', stacklevel=5)
            headers['Content-Type'] = 'application/json;charset=UTF-8'
        if data:
            body, content_type = self._encode_data_to_form_data(data)
            headers['Content-Type'] = content_type
            if self.debug:
                self._logger.info(f'Form data - {data}', stacklevel=5)
        index, conn = self.__get_connection()
        headers.update(self.headers)
        conn.request(method, url, body=body, headers=headers)
        response = FastResponse(conn.getresponse())
        self._connections[index][1] = False
        return response

    def get(self, url, *, params=None, headers=None):
        return self.request('GET', url, params=params, headers=headers)

    def post(self, url, *, data=None, json=None, headers=None):
        return self.request('POST', url, data=data, json=json, headers=headers)

    def put(self, url, *, data=None, headers=None):
        return self.request('PUT', url, data=data, headers=headers)

    def delete(self, url, *, data=None, headers=None):
        return self.request('DELETE', url, data=data, headers=headers)

    def close(self):
        for connection, status in self._connections:
            connection.close()
        self._connections.clear()
        self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor

    client = FastHTTPClient('http://127.0.0.1:8087', debug=False)

    @logger.catch_exception
    def search():
        for _ in range(10000):
            client.get('/')


    @debug
    def main():
        with ThreadPoolExecutor(max_workers=10) as executor:
            for _ in range(10):
                executor.submit(search)

    main()

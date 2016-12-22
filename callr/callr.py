###
# CALLR webservice communication library
###

from future import standard_library
standard_library.install_aliases()
from past.builtins import basestring
from builtins import object
import sys, platform
import json
import urllib.request, urllib.error, urllib.parse
import base64
from random import randint

PY3 = sys.version_info[0] >= 3

def base64encode(bytes_or_str):
    if PY3 and isinstance(bytes_or_str, str):
        input_bytes = bytes_or_str.encode('utf8')
    else:
        input_bytes = bytes_or_str

    output_bytes = base64.b64encode(input_bytes)
    if PY3:
        return output_bytes.decode('ascii')
    else:
        return output_bytes

class Api(object):
    SDK_VERSION = "2.0.1"

    _api_url = "https://api.thecallr.com/"
    _login = False
    _password = False
    _headers = {
        "Expect": "",
        "Content-Type": "application/json-rpc; charset=utf-8",
        "User-Agent": "sdk=PYTHON; sdk-version=%s; lang-version=%s; platform=%s" % (SDK_VERSION, platform.python_version(), platform.system()),
    }
    
    ###
    # Initialization
    # @param string login
    # @param string password
    ###
    def __init__(self, login, password, options = None):
        self._login = login
        self._password = password
        self.set_options(options)

    def set_options(self, options):
        if isinstance(options, dict):
            if "proxy" in options:
                self.set_proxy(options["proxy"])

    def set_proxy(self, proxy):
        if isinstance(proxy, basestring):
            proxy_handler = urllib.request.ProxyHandler({'https': proxy})
            opener = urllib.request.build_opener(proxy_handler)
            urllib.request.install_opener(opener)
        else:
            raise CallrLocalException("PROXY_NOT_STRING", 1)

    def set_api_url(self, url):
        if isinstance(url, basestring):
            self._api_url = url
        else: 
            raise CallrLocalException("URL_NOT_STRING", 1)

    ###
    # Send a request to CALLR webservice
    ###
    def call(self, method, *params):
        return self.send(method, params)

    ###
    # Send a request to CALLR webservice
    ###
    def send(self, method, params = [], id = None):
        self._check_auth()

        json_data = json.dumps({
            "id": (id, randint(100, 999))[id is None],
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }).encode('utf8')

        self._headers["Authorization"] = "Basic %s" % base64encode('%s:%s' % (self._login, self._password)).replace('\n', '')

        req = urllib.request.Request(self._api_url, json_data, self._headers)
        try:
            res = urllib.request.urlopen(req)
            if res.code != 200:
                raise CallrException("HTTP_CODE_ERROR", -1, {"http_code": res.code, "http_message": res.msg})
            return self._parse_response(res.read())
        except urllib.error.HTTPError as e:
            raise CallrException("HTTP_CODE_ERROR", -1, {"http_code": e.code, "http_message": e.msg})
        except urllib.error.URLError as e:
            raise CallrException("HTTP_EXCEPTION", -2, {"exception": e})


    def _check_auth(self):
        if self._login is None or len(self._login) == 0 or self._password is None or len(self._password) == 0:
            raise CallrLocalException("CREDENTIALS_NOT_SET", 1)

    ###
    # Response analysis
    ###
    def _parse_response(self, body):
        try:
            if isinstance(body, str):
                data = json.loads(body)
            else: 
                data = json.loads(str(body, 'utf-8'))				

            if data and "result" in data:
                return data["result"]
            elif data and "error" in data and data["error"]:
                raise CallrException(data["error"]["message"], data["error"]["code"])
            else:
                raise CallrException("INVALID_RESPONSE", -2, {"response": body})
        except ValueError as e:
            print(e)
            raise CallrException("INVALID_RESPONSE", -2, {"response": body})


###
# Exceptions
###
class CallrException(Exception):
    def __init__(self, msg, code = 0, data = None):
        self.msg = msg
        self.code = code
        self.data = data

class CallrLocalException(CallrException):
    pass

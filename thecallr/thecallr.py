###
# THECALLR webservice communication library
###

import json
import urllib2
from base64 import encodestring
from random import randint

class Api(object):
	_login = False
	_password = False
	_headers = {
		"Expect": "",
		"Content-Type": "application/json-rpc; charset=utf-8"
	}

	API_URL = "https://api.thecallr.com/"

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
			if options.has_key("proxy"):
				self.set_proxy(options["proxy"])

	def set_proxy(self, proxy):
		if isinstance(proxy, basestring):
			proxy_handler = urllib2.ProxyHandler({'https': proxy})
			opener = urllib2.build_opener(proxy_handler)
			urllib2.install_opener(opener)
		else:
			raise ThecallrLocalException("PROXY_NOT_STRING", 1)

	###
	# Send a request to THECALLR webservice
	###
	def call(self, method, *params):
		self.send(method, params)

	###
	# Send a request to THECALLR webservice
	###
	def send(self, method, params = [], id = None):
		self._check_auth()

		json_data = json.dumps({
			"id": (id, randint(100, 999))[id is None],
			"jsonrpc": "2.0",
			"method": method,
			"params": params
		})

		self._headers["Authorization"] = "Basic %s" % encodestring('%s:%s' % (self._login, self._password)).replace('\n', '')

		req = urllib2.Request(self.API_URL, json_data, self._headers)
		try:
			res = urllib2.urlopen(req)
			if res.code != 200:
				raise ThecallrException("HTTP_CODE_ERROR", -1, {"http_code": res.code, "http_message": res.msg})
			return self._parse_response(res.read())
		except urllib2.HTTPError as e:
			raise ThecallrException("HTTP_CODE_ERROR", -1, {"http_code": e.code, "http_message": e.msg})
		except urllib2.URLError as e:
			raise ThecallrException("HTTP_EXCEPTION", -2, {"exception": e})


	def _check_auth(self):
		if self._login == False or len(self._login) == 0 or self._password == False or len(self._password) == 0:
			raise ThecallrLocalException("CREDENTIALS_NOT_SET", 1)

	###
	# Response analysis
	###
	def _parse_response(self, body):
		try:
			data = json.loads(body)
			if data and data.has_key("result") and data["result"]:
				return data["result"]
			elif data and data.has_key("error") and data["error"]:
				raise ThecallrException(data["error"]["message"], data["error"]["code"])
			else:
				raise ThecallrException("INVALID_RESPONSE", -2, {"response": body})
		except ValueError as e:
			raise ThecallrException("INVALID_RESPONSE", -2, {"response": body})


###
# Exceptions
###
class ThecallrException(Exception):
	def __init__(self, msg, code = 0, data = None):
		self.msg = msg
		self.code = code
		self.data = data

class ThecallrLocalException(ThecallrException):
	pass

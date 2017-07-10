import http.client
import json
from urllib3.util import parse_url


def get_request(scheme, host, endpoint, method, headers):
	if scheme == "https":
		connection = http.client.HTTPSConnection(host)
	else:
		connection = http.client.HTTPConnection(host)
	connection.request(method=method, url="{}".format(endpoint), headers=headers)
	raw_response = connection.getresponse()
	return raw_response


def _explode_and_get(url, headers):
	url_parts = parse_url(url)
	host = url_parts.hostname
	endpoint = url_parts.request_uri
	scheme = url_parts.scheme
	method = "GET"
	return get_request(scheme=scheme, host=host, endpoint=endpoint, method=method, headers=headers)


def get_json(url):
	headers = {
		"Accept": "*/*",
		"Content-Type": "application/json",
		"Connection": "keep-alive",
	}
	raw_response = _explode_and_get(url=url, headers=headers)
	return json.loads(raw_response.read().decode("utf-8"))


def get(url):
	headers = {
		"Accept": "*/*",
		"Content-Type": "text/html",
		"Connection": "keep-alive",
	}
	raw_response = _explode_and_get(url=url, headers=headers)
	return raw_response.read().decode("utf-8")

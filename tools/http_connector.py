"""Basic http connector to avoid requiring dependencies."""
from urllib3.util import parse_url
import http.client
import zipfile
import logging
import json
import io


def get_request(scheme, host, endpoint, method, headers):
	raw_response = None
	for retry in range(0, 3):
		try:
			if scheme == "https":
				connection = http.client.HTTPSConnection(host, timeout=5)
			else:
				connection = http.client.HTTPConnection(host, timeout=5)
			connection.request(method=method, url=endpoint, headers=headers)
			raw_response = connection.getresponse()
			return raw_response
		except:
			print("Connection attempt {} to host '{}' failed...".format(retry, host))
	return raw_response


def _explode_and_get(url, headers):
	url_parts = parse_url(url)
	host = url_parts.hostname
	endpoint = url_parts.request_uri
	scheme = url_parts.scheme
	method = "GET"
	stream = get_request(scheme=scheme, host=host, endpoint=endpoint, method=method, headers=headers)
	return stream.read()


def get_text(url):
	headers = {
		"Accept": "*/*",
		"Content-Type": "text/html",
		"Connection": "keep-alive",
	}
	raw_response = _explode_and_get(url=url, headers=headers)
	if not raw_response:
		return "?"
	return raw_response.decode("utf-8")


def get_json(url):
	headers = {
		"Accept": "*/*",
		"Content-Type": "application/json",
		"Connection": "keep-alive",
	}
	raw_response = _explode_and_get(url=url, headers=headers)
	if not raw_response:
		return {}
	json_string = raw_response.decode("utf-8")
	return json.loads(json_string)


def get_zip_file(url):
	headers = {
		"Accept": "*/*",
		"Content-Type": "text/html",
		"Connection": "keep-alive",
	}
	raw_response = _explode_and_get(url=url, headers=headers)
	if not raw_response:
		return None
	fp = io.BytesIO(raw_response)
	return zipfile.ZipFile(file=fp)

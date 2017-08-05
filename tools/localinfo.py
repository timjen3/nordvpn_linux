from nordvpn.nordvpn_linux_models import LocaleInfo
from tools.http_connector import get_json
from tools.http_connector import get_text


def get_ip():
	"""Returns WAN ip"""
	response = get_text('https://api.ipify.org')
	return response


def get_meta():
	"""Loads WAN IP and uses a site to load locale data about it."""
	ip = get_ip()
	url = "http://ip-api.com/json/{}".format(ip)
	meta = get_json(url=url)
	return LocaleInfo(
		ip=ip,
		country=meta["country"],
		zipcode=meta["zip"],
		latitude=meta["lat"],
		longitude=meta["lon"],
		region=meta["regionName"],
		city=meta["city"],
		isp=meta["org"],
	)

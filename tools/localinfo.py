from nordvpn.nordvpn_linux_models import LocaleInfo, LocaleInfo2
from tools.http_connector import get_json
from tools.http_connector import get_text


def get_meta2():
	"""Not as much data, but 1/2 api calls and 1/2 dependencies. Using this whenever possible. Still need the original
	for purpose of Server ranking, but for any other checks this is adequate."""
	# uuid4 doesn't seem to be working as expected on linux, so for now just using simple redirect.
	# import uuid
	# random_string = str(uuid.uuid4()).replace("-", "")
	# ip_meta = get_json(url="http://{}.edns.ip-api.com/json".format(random_string))
	ip_meta_url = "http://edns.ip-api.com/json"
	ip_meta = get_json(url=ip_meta_url)
	return LocaleInfo2(
		dns_ip=ip_meta.get("dns", dict()).get("ip", ""),
		dns_ip_geo=ip_meta.get("dns", dict()).get("geo", ""),
		ip=ip_meta.get("edns", dict()).get("ip", ""),
		ip_geo=ip_meta.get("edns", dict()).get("geo", ""),
	)


def get_ip():
	current_ip = get_text('https://api.ipify.org')
	return current_ip


def get_meta():
	"""Loads WAN IP and uses a site to load locale data about it."""
	current_ip = get_ip()
	url = "http://ip-api.com/json/{}".format(current_ip)
	meta = get_json(url=url)
	return LocaleInfo(
		ip=current_ip,
		country=meta["country"],
		zipcode=meta["zip"],
		latitude=meta["lat"],
		longitude=meta["lon"],
		region=meta["regionName"],
		city=meta["city"],
		isp=meta["org"],
	)

from nordvpn import nordvpn_connector, ovpn_connector
from tools import localinfo, filter_ranker
from nordvpn.load_content import NordVpnServerData
from datetime import datetime, timedelta
import time
import json
import sys
import os


def get_ranked_servers(server_meta_data, locale_meta_data, max_load):
	"""
	:param server_meta_data: VPN Server meta data loaded into a list of Server()
	:param locale_meta_data: Your location as LocaleInfo()
	:return: list of Server() sorted by distance, load
	"""
	SR = filter_ranker.ServerRanker(locale_meta_data)
	SR.load(server_meta_data)
	SR.sort()
	SR.filter(max_load)
	return SR.servers


def refresh_server_data(config):
	"""Return existing data if less than 7 days old, else return new data. If new data is unavailable return
	existing data regardless."""
	PD = NordVpnServerData(config)
	if PD.server_data is not None and PD.server_data["date"] > datetime.utcnow() - timedelta(days=7):
		return PD.server_data["data"]
	servers = nordvpn_connector.servers(url=config["nord_server_meta_url"])
	locale_data = localinfo.get_meta()
	data = get_ranked_servers(servers, locale_data, 40)
	if data is not None:
		PD.write(data)
		return data
	if PD.server_data is not None:
		return PD.server_data["data"]
	return []


if __name__ == "__main__":
	#  Open tool config
	os.environ["APPLICATION_ROOT"] = sys.argv[0]
	config_path = os.sep.join(["content", "tool.json"])
	with open(config_path, "r") as fp:
		tool_config = json.loads(fp.read())

	#  Load server metadata
	servers = refresh_server_data(tool_config)
	num_results = tool_config["iter_results"]

	#  Endlessly iterate over the first X server results
	while True:
		for s in servers[0:num_results]:
			print("Connecting to a server...\n\tDomain: {}\n\tDistance Class: {}\n\tLoad Class: {}\n\tFile Path: {}\n".format(
				s.domain,
				s.distance_class,
				s.load_class,
				ovpn_connector.get_ovpn_file_path(domain_name=s.domain)
			))
			ovpn_connector.process_ovpn_file(s.domain, tool_config)
			print("Disconnected from server...Reconnecting to a new server in 5 seconds.")
			time.sleep(5)

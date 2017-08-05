from nordvpn.nordvpn_connector import ServerManager
from tools.speed_test import get_avg_ping
from openvpn import openvpn_connector
from tools import localinfo
import threading
import json
import time
import logging
import os
logging.basicConfig(
	level=logging.DEBUG,
	format='%(asctime)s %(levelname)s {%(pathname)s:%(lineno)d} %(message)s',
	handlers=[logging.StreamHandler()],
)


def get_new_ip_meta(old_meta, kill_me):
	# TODO: If ovpn fails to connect and wants to try a new server exit.
	current_meta = localinfo.get_meta()
	while old_meta.ip == current_meta.ip or kill_me["kill"]:
		time.sleep(5)
		current_meta = localinfo.get_meta()
	return current_meta


def connect_to_fastest_server_looped():
	"""Keeps you connected to the closest/fastest vpn as long as process is running."""
	os.environ["APPLICATION_ROOT"] = os.getcwd()
	logger = logging.getLogger("NORDVPNLINUX")
	SM = ServerManager(config=tool_config)
	for server in SM.servers:
		response_time = get_avg_ping(server.ip)
		target_server_stats = "\n\t".join([
			"Domain: {}".format(server.domain),
			"Avg Response Time: {} ms".format(response_time),
			"Distance: {} mi".format(server.distance),
			"Distance Class: {}".format(server.distance_class),
			"Load: {}".format(server.load),
			"Features: {}".format(",".join([k for k, v in server.features.items() if v])),  # List server features
			"Categories: {}".format(server.categories),
			"Search Keywords: {}".format(server.search_keywords),
			"File: {}".format(openvpn_connector.get_ovpn_file_path(domain_name=server.domain, config=tool_config))
		])
		if response_time >= tool_config["max_response_time"]:
			logger.debug("Skipping a server because it is responding too slowly:\n\t" + target_server_stats)
		else:
			logger.info("Connecting to server via vpn tunnel...\n\t" + target_server_stats)
			kill_me = {"kill": False}
			start_vpn_fun = lambda d, c, f: openvpn_connector.start_vpn_service(d, c, f)
			t = threading.Thread(target=start_vpn_fun(server.domain, tool_config, kill_me))
			get_new_ip_info = lambda o, f: get_new_ip_meta(o, f)
			t2 = threading.Thread(target=get_new_ip_info(SM.locale_data, kill_me))
			t.start()
			t2.start()
			locale_meta = t2.join()
			new_ip_meta = "\n\t".join([
				"Country: {}".format(locale_meta.country),
				"Zipcode: {}".format(locale_meta.zipcode),
				"Region: {}".format(locale_meta.region),
				"City: {}".format(locale_meta.city),
				"ISP: {}".format(locale_meta.isp),
			])
			logger.info("Connected to vpn:\n\t" + new_ip_meta)
			t.join()


if __name__ == "__main__":
	config_path = os.sep.join(["content", "tool.json"])
	with open(config_path, "r") as fp:
		tool_config = json.loads(fp.read())

	connect_to_fastest_server_looped()

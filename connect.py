# TODO: Add a kill switch please!!!
from nordvpn.nordvpn_connector import ServerManager
from tools.speed_test import get_avg_ping
from openvpn import openvpn_connector
import logging
import json
import os
logging.basicConfig(
	level=logging.DEBUG,
	format='%(asctime)s %(levelname)s {%(pathname)s:%(lineno)d} %(message)s',
	handlers=[logging.StreamHandler()],
)


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
			openvpn_connector.start_vpn_service(server.domain, tool_config, SM.locale_data)


if __name__ == "__main__":
	config_path = os.sep.join(["content", "tool.json"])
	with open(config_path, "r") as fp:
		tool_config = json.loads(fp.read())
	connect_to_fastest_server_looped()

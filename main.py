from nordvpn.nordvpn_connector import ServerManager
from nordvpn import openvpn_connector
import json
import os
import logging


if __name__ == "__main__":
	"""Keeps you connected to the closest/fastest vpn as long as it's running."""
	logging.basicConfig(
		level=logging.INFO,
		format='%(asctime)s %(levelname)s {%(pathname)s:%(lineno)d} %(message)s',
		handlers=[logging.StreamHandler()],
	)
	config_path = os.sep.join(["content", "tool.json"])
	with open(config_path, "r") as fp:
		tool_config = json.loads(fp.read())
	os.environ["APPLICATION_ROOT"] = os.getcwd()
	logger = logging.getLogger("NORDVPNLINUX")

	SM = ServerManager(config=tool_config)
	for server in SM.servers:
		logger.info("\n\t".join([
			"Connecting vpn...",
			"Domain: {}".format(server.domain),
			"Distance: {}".format(server.distance),
			"Distance Class: {}".format(server.distance_class),
			"Load: {}".format(server.load),
			"Features: {}".format(",".join([k for k, v in server.features.items() if v])),  # List server features
			"File: {}".format(openvpn_connector.get_ovpn_file_path(domain_name=server.domain, config=tool_config))
		]))
		openvpn_connector.process_openvpn_file(server.domain, tool_config)

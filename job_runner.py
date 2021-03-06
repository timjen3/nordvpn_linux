from nordvpn.nordvpn_connector import ServerManager
from tools.speed_test import get_avg_ping
from openvpn import openvpn_connector
from tools.threading import threaded
from tools.localinfo import get_meta
from tools.linux import pid_exists
import logging
import json
import os
__TOOL_CONFIG__ = None


class Static:
	def __init__(self, cls):
		cls()


@Static
class JobRunner:
	__TOOL_CONFIG__ = None

	def __init__(self):
		with open("content/tool.json", "r") as fp:
			config = json.loads(fp.read())
		global __TOOL_CONFIG__
		__TOOL_CONFIG__ = config


@threaded
def connect_vpn():
	os.environ["APPLICATION_ROOT"] = os.getcwd()
	logger = logging.getLogger("NORDVPNLINUX")
	SM = ServerManager(config=__TOOL_CONFIG__)
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
			"File: {}".format(openvpn_connector.get_ovpn_file_path(domain_name=server.domain, config=__TOOL_CONFIG__))
		])
		if response_time >= __TOOL_CONFIG__["max_response_time"]:
			logger.debug("Skipping a server because it is responding too slowly:\n\t" + target_server_stats)
		else:
			logger.info("Connecting to server via vpn tunnel...\n\t" + target_server_stats)
			openvpn_connector.connect(server.domain, __TOOL_CONFIG__, SM.locale_data)
			t = check_alive()
			return t.result_queue.get()


@threaded
def disconnect_function():
	openvpn_connector.disconnect()
	t = check_alive()
	return t.result_queue.get()


@threaded
def check_alive():
	"""Checks if process defined in pid file is alive."""
	is_alive = False
	if "pid_file" in __TOOL_CONFIG__ and os.path.exists(__TOOL_CONFIG__["pid_file"]):
		with open(__TOOL_CONFIG__["pid_file"], "r") as fp:
			pid = fp.read().strip(" \r\n")
			if pid.isdigit():
				pid = int(pid)
			else:
				pid = -1
			is_alive = pid_exists(pid)
	locale_info = get_meta()
	return is_alive, locale_info.serializable

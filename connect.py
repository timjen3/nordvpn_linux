# TODO: Add a kill switch please!!!
from nordvpn.nordvpn_connector import ServerManager
from tools.speed_test import get_avg_ping
from openvpn import openvpn_connector
from tools.threading import threaded
from tools.localinfo import get_meta
from tools.linux import pid_exists
import traceback
import logging
import json
import os


@threaded
def connect_vpn():
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
	if "pid_file" in tool_config and os.path.exists(tool_config["pid_file"]):
		pid = open(tool_config["pid_file"], "r").read()
		if pid.isdigit():
			pid = int(pid)
		else:
			pid = -1
		is_alive = pid_exists(pid)
	locale_info = get_meta()
	return is_alive, "IP:{}\nREGION:{}".format(locale_info.ip, locale_info.region)


if __name__ == "__main__":
	from gui.simple_gui import start_gui

	try:
		config_path = os.sep.join(["content", "tool.json"])
		with open(config_path, "r") as fp:
			tool_config = json.loads(fp.read())

		app_log_dir = tool_config.get("application_log", "")
		application_log_path = "{}{}".format(app_log_dir, "application.log")
		logging.basicConfig(
			level=logging.DEBUG,
			format='%(asctime)s %(levelname)s {%(pathname)s:%(lineno)d} %(message)s',
			handlers=[logging.StreamHandler(), logging.FileHandler(filename=application_log_path, mode="w")],
		)
		locale_info = get_meta()
		local_msg = "IP:{}\nREGION:{}".format(locale_info.ip, locale_info.region)
		start_gui(start_fun=connect_vpn, stop_fun=disconnect_function, alive_fun=check_alive, locale_info=local_msg)
	except:
		logger = logging.getLogger(__name__)
		logger.critical("Program crashed!\n{}".format(traceback.format_exc()))

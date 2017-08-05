"""Launches vpn connection using NordVPN ovpn connection file. Supports passing optional arguments.
Does some fancy threading to output new connection info after getting connected."""
from tools.linux import send_desktop_msg
from tools import localinfo
import subprocess
import threading
import logging
import time
import os


def get_new_ip_meta(old_meta, stop_flag):
	logger = logging.getLogger(__name__)
	current_meta = localinfo.get_meta()
	send_desktop_msg("trying in a sec.")
	while old_meta.ip == current_meta.ip and not stop_flag["stop"]:
		logger.info(old_meta.ip)
		logger.info(current_meta.ip)
		time.sleep(5)
		current_meta = localinfo.get_meta()
	send_desktop_msg("got this far...")
	msg = " ".join([
		"Old IP: {}".format(old_meta.ip),
		"New IP: {}".format(current_meta.ip),
		"Country: {}".format(current_meta.country),
		"Zipcode: {}".format(current_meta.zipcode),
		"Region: {}".format(current_meta.region),
		"City: {}".format(current_meta.city),
		"ISP: {}".format(current_meta.isp),
	])
	send_desktop_msg("VPN CONNECTED: {}'".format(msg))


def _get_formatted_sh_script(ovpn_config_file_path, args):
	for arg in args:
		if "--config " in arg:
			return "sudo openvpn {}".format(" ".join(arg for arg in args))  # User specifies specific --config
	openvpn_connect_sh = "sudo openvpn --config {} {}".format(
		ovpn_config_file_path,
		" ".join(arg for arg in args)
	)
	return openvpn_connect_sh


def get_ovpn_file_path(domain_name, config):
	application_root = os.environ["APPLICATION_ROOT"]
	if config.get("connect") == "tcp":
		file_name = "{}.tcp443.ovpn".format(domain_name)
	else:
		file_name = "{}.udp1194.ovpn".format(domain_name)
	return os.sep.join([application_root, "content", "ovpnfiles", file_name])


def _process_openvpn_file(domain_name, config):
	absolute_path = get_ovpn_file_path(domain_name=domain_name, config=config)
	prepared_sh_script = _get_formatted_sh_script(ovpn_config_file_path=absolute_path, args=config["cli_args"])
	ps = subprocess.Popen(prepared_sh_script, shell=True)
	ps.communicate()
	ps.wait()


# TODO: Add a kill switch please!!!
# subprocess.Popen("content/vpn_up.sh")
# subprocess.Popen("content/vpn_down.sh")
def start_vpn_service(domain_name, config, old_meta):
	"""Connect vpn and output new connection information. B/c the first thing you want to see is whether it
	actually worked! Every damn time..."""
	os.popen("notify-send 'Old IP: {}'".format(old_meta.ip))

	thread_state = {"stop": False}
	connect_vpn_fun = lambda d, c: _process_openvpn_file(d, c)
	connect_vpn = threading.Thread(target=connect_vpn_fun(domain_name, config), daemon=False)
	output_connection_fun = lambda m, f: get_new_ip_meta(m, f)
	output_connection_info = threading.Thread(target=output_connection_fun(old_meta, thread_state), daemon=True)
	output_connection_info.start()

	connect_vpn.start()
	connect_vpn.join()
	thread_state["stop"] = True

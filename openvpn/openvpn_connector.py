"""Launches vpn connection using NordVPN ovpn connection file. Supports passing optional arguments."""
from tools import localinfo
import subprocess
import threading
import logging
import time
import os


def get_new_ip_meta(old_meta):
	logger = logging.getLogger(__name__)
	current_meta = localinfo.get_meta()
	while old_meta.ip == current_meta.ip:
		time.sleep(5)
		current_meta = localinfo.get_meta()
	logger.info("Connected to server successfully.\n\t".join([
		"Country: {}".format(current_meta.country),
		"Zipcode: {}".format(current_meta.zipcode),
		"Region: {}".format(current_meta.region),
		"City: {}".format(current_meta.city),
		"ISP: {}".format(current_meta.isp),
	]))


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


# subprocess.Popen("content/vpn_up.sh")
# subprocess.Popen("content/vpn_down.sh")
def start_vpn_service(domain_name, config, old_meta):
	start_vpn_fun = lambda d, c: _process_openvpn_file(d, c)
	t = threading.Thread(target=start_vpn_fun(domain_name, config))
	t.start()
	output_connection_fun = lambda m: get_new_ip_meta(m)
	t2 = threading.Thread(target=output_connection_fun(old_meta))
	t2.start()
	t.join()
	t2._stop()

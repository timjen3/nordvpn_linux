"""Launches vpn connection using NordVPN ovpn connection file. Supports passing optional arguments."""
from tools.linux import send_desktop_msg
from tools import localinfo
import subprocess
import time
import os


def get_new_ip_meta(old_ip):
	current_ip = localinfo.get_ip()
	send_desktop_msg("got this far...")
	while old_ip == current_ip:
		time.sleep(5)
		current_ip = localinfo.get_ip()
	send_desktop_msg("got this far...")
	msg = "VPN CONNECTED: {}".format(current_ip)
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
	print("started vpn....")


# TODO: Add a kill switch please!!!
# subprocess.Popen("content/vpn_up.sh")
# subprocess.Popen("content/vpn_down.sh")
def start_vpn_service(domain_name, config, old_meta):
	"""Connect vpn and output new connection information. B/c the first thing you want to see is whether it
	actually worked! Every damn time..."""
	old_ip = old_meta.ip
	_process_openvpn_file(domain_name, config)
	get_new_ip_meta(old_ip)

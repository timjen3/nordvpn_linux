"""Launches vpn connection using NordVPN ovpn connection file. Supports passing optional arguments."""
from tools.linux import send_desktop_msg
from tools import localinfo
import subprocess
import time
import os
import sys


def sentry(old_meta):
	current_meta = localinfo.get_meta()
	while old_meta.ip == current_meta.ip:
		time.sleep(5)
		current_meta = localinfo.get_meta()
	send_desktop_msg("got this far...")
	msg = "VPN CONNECTED: IP: {}=>{}; Region: {}=>{};".format(current_meta.ip, old_meta.ip, current_meta.region, old_meta.region)
	send_desktop_msg(msg)
	sys.exit()


def _get_formatted_sh_script(ovpn_config_file_path, args):
	base_command = "sudo openvpn"
	user_specified_config_target = "--config" in [arg for arg in args]
	if user_specified_config_target:
		openvpn_connect_sh = "{} {}".format(
			base_command,
			" ".join(arg for arg in args)
		)
	else:
		openvpn_connect_sh = "{} --config {} {}".format(
			base_command,
			ovpn_config_file_path,
			" ".join(arg for arg in args)
		)
	background_command = "nohup {} &".format(openvpn_connect_sh)
	return background_command


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
	_process_openvpn_file(domain_name, config)
	sentry(old_meta)

"""Launches vpn connection using NordVPN ovpn connection file. Supports passing optional arguments."""
from tools.linux import send_desktop_msg
from tools import localinfo
from copy import copy
import subprocess
import time
import os


def sentry(old_meta):
	"""Notifies when connected and monitors to ensure remains connected. If disconnected notifies desktop and returns.
	:param old_meta: locale info from before connecting to vpn.
	"""
	current_meta = localinfo.get_meta()
	while old_meta.ip == current_meta.ip:
		time.sleep(5)
		current_meta = localinfo.get_meta()
	vpn_meta = copy(current_meta)
	msg = "VPN CONNECTED! IP: {}=>{}; Region: {}=>{};".format(old_meta.ip, current_meta.ip, old_meta.region, current_meta.region)
	send_desktop_msg(msg, delay=3000)
	while current_meta.ip == vpn_meta.ip:
		time.sleep(15)
		current_meta = localinfo.get_meta()
	msg = "VPN DISCONNECTED! IP: {}=>{}; Region: {}=>{};".format(vpn_meta.ip, current_meta.ip, vpn_meta.region, current_meta.region)
	send_desktop_msg(msg, delay=3000)


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


def start_vpn_service(domain_name, config, old_meta):
	os.popen("sudo killall openvpn")
	_process_openvpn_file(domain_name, config)
	sentry(old_meta)

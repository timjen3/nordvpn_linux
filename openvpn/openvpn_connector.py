"""Launches vpn connection using NordVPN ovpn connection file. Supports passing optional arguments."""
from tools import localinfo
from tools import linux
import time
import os


def watchdog(vpn_meta):
	current_meta = localinfo.get_meta()
	while current_meta.ip == vpn_meta.ip:
		time.sleep(15)
		current_meta = localinfo.get_meta()
	msg = "VPN DISCONNECTED! IP: {}=>{}; Region: {}=>{};".format(vpn_meta.ip, current_meta.ip, vpn_meta.region, current_meta.region)
	linux.send_desktop_msg(msg, delay=3000)


def disconnect():
	current_meta = localinfo.get_meta()
	linux.execute_and_wait("gksudo killall openvpn")
	linux.execute_and_wait("gksudo service networking restart")
	new_meta = localinfo.get_meta()
	msg = "VPN DISCONNECTED! IP: {}=>{}; Region: {}=>{};".format(current_meta.ip, new_meta.ip, current_meta.region, new_meta.region)
	linux.send_desktop_msg(msg, delay=3000)


def ensure_connect(pid, old_meta):
	current_meta = localinfo.get_meta()
	while old_meta.ip == current_meta.ip:
		time.sleep(3)
		current_meta = localinfo.get_meta()
	msg = "VPN CONNECTED! IP: {}=>{}; Region: {}=>{};".format(old_meta.ip, current_meta.ip, old_meta.region, current_meta.region)
	linux.send_desktop_msg(msg, delay=3000)
	# watchdog(current_meta)  # TODO: reconnect auto?


def _get_formatted_sh_script(ovpn_config_file_path, args):
	base_command = "sudo openvpn --cd {}".format(os.environ["APPLICATION_ROOT"])
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
	pid = linux.execute_no_wait(prepared_sh_script)
	return pid


def start_vpn_service(domain_name, config, old_meta):
	pid = _process_openvpn_file(domain_name, config)
	ensure_connect(pid, old_meta)

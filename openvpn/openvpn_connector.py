"""Launches vpn connection using NordVPN ovpn connection file. Supports passing optional arguments."""
from tools import localinfo
from tools import linux
import time
import os


def connect(domain_name, config, old_meta):
	absolute_path = get_ovpn_file_path(domain_name=domain_name, config=config)
	prepared_sh_script = _get_formatted_sh_script(ovpn_config_file_path=absolute_path, config=config)
	linux.execute_and_wait(prepared_sh_script, timeout=10)
	for retry in range(0, 3):
		current_ip = localinfo.get_ip()
		if old_meta.ip != current_ip:
			linux.send_desktop_msg("VPN connected: {}".format(current_ip), delay=3000)
			return
		time.sleep(7)
	raise Exception("Failed to connect to VPN!")


def disconnect():
	pre_ip = localinfo.get_ip()
	linux.execute_and_wait("gksudo killall openvpn", timeout=60)
	linux.execute_and_wait("gksudo service networking restart", timeout=60)
	post_ip = localinfo.get_ip()
	msg = "VPN DISCONNECTED! IP: {}=>{};".format(pre_ip, post_ip)
	linux.send_desktop_msg(msg, delay=3000)


def _get_formatted_sh_script(ovpn_config_file_path, config):
	args = config["cli_args"]
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
	pidarg = "--writepid {}".format(config["pid_file"])
	return "{} {}".format(openvpn_connect_sh, pidarg)


def get_ovpn_file_path(domain_name, config):
	application_root = os.environ["APPLICATION_ROOT"]
	if config.get("connect") == "tcp":
		file_name = "{}.tcp443.ovpn".format(domain_name)
	else:
		file_name = "{}.udp1194.ovpn".format(domain_name)
	return os.sep.join([application_root, "content", "ovpnfiles", file_name])

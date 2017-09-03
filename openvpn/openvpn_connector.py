"""Launches vpn connection using NordVPN ovpn connection file. Supports passing optional arguments."""
from tools.threading import threaded
from tools.linux import pid_exists
from tools import localinfo
from tools import linux
import time
import os


@threaded
def watchdog(vpn_meta):
	# TODO: Here's an idea... 1. start watchdog in new thread and 2. use sys.argv to start the vpn back up if it dies.
	# 		Then can create a systemd service.
	current_meta = localinfo.get_meta()
	while current_meta.ip == vpn_meta.ip:
		time.sleep(60)
		current_meta = localinfo.get_meta()
	msg = "VPN DISCONNECTED! IP: {}=>{}; Region: {}=>{};".format(vpn_meta.ip, current_meta.ip, vpn_meta.region, current_meta.region)
	linux.send_desktop_msg(msg, delay=3000)


def disconnect():
	current_meta = localinfo.get_meta()
	linux.execute_and_wait("gksudo killall openvpn")
	linux.execute_and_wait("gksudo service networking restart")
	time.sleep(3)  # ensure network is re-connected to prevent hanging...
	new_meta = localinfo.get_meta()
	msg = "VPN DISCONNECTED! IP: {}=>{}; Region: {}=>{};".format(current_meta.ip, new_meta.ip, current_meta.region, new_meta.region)
	linux.send_desktop_msg(msg, delay=3000)


def ensure_connect(pid, old_meta):
	current_meta = localinfo.get_meta()
	while pid_exists(pid) and old_meta.ip == current_meta.ip:
		time.sleep(3)
		current_meta = localinfo.get_meta()
	if old_meta.ip != current_meta.ip:
		msg = "VPN CONNECTED! IP: {}=>{}; Region: {}=>{};".format(old_meta.ip, current_meta.ip, old_meta.region, current_meta.region)
	else:
		msg = "VPN FAILED TO CONNECT! IP: {}=>{}; Region: {}=>{};".format(old_meta.ip, current_meta.ip, old_meta.region, current_meta.region)
	linux.send_desktop_msg(msg, delay=3000)
	# watchdog(current_meta)  # TODO: reconnect auto?


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
	if "pid_file" not in config:
		return "nohup {} &".format(openvpn_connect_sh)
	else:
		pidarg = "--writepid {}".format(config["pid_file"])
		return "nohup {} {} &".format(openvpn_connect_sh, pidarg)


def get_ovpn_file_path(domain_name, config):
	application_root = os.environ["APPLICATION_ROOT"]
	if config.get("connect") == "tcp":
		file_name = "{}.tcp443.ovpn".format(domain_name)
	else:
		file_name = "{}.udp1194.ovpn".format(domain_name)
	return os.sep.join([application_root, "content", "ovpnfiles", file_name])


def _process_openvpn_file(domain_name, config):
	absolute_path = get_ovpn_file_path(domain_name=domain_name, config=config)
	prepared_sh_script = _get_formatted_sh_script(ovpn_config_file_path=absolute_path, config=config)
	pid = linux.execute_no_wait(prepared_sh_script)
	return pid


def start_vpn_service(domain_name, config, old_meta):
	pid = _process_openvpn_file(domain_name, config)
	ensure_connect(pid, old_meta)
	return pid

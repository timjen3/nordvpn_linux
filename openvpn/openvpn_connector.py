"""Launches vpn connection using NordVPN ovpn connection file. Supports passing optional arguments."""
from tools.threading import threaded
from tools.linux import pid_exists
from tools import localinfo
from tools import linux
import logging
import time
import os


@threaded
def watchdog(vpn_meta):
	# TODO: Get watchdog working and add option to gui!
	# TODO: Here's an idea... 1. start watchdog in new thread and 2. use sys.argv to start the vpn back up if it dies.
	# 		Then can create a systemd service.
	current_ip = localinfo.get_ip()
	# TODO: Check if openvpn is running instead of relying on api.
	# TODO: After some initial investigation, a kill switch will be hard. Will investigate after other todo's.
	current_meta = vpn_meta
	while vpn_meta.ip == current_ip:
		time.sleep(60)
		current_meta = localinfo.get_meta2()
	msg = "VPN DISCONNECTED! IP: {}=>{}; Region: {}=>{};".format(vpn_meta.ip, current_meta.ip, vpn_meta.ip_geo, current_meta.ip_geo)
	linux.send_desktop_msg(msg, delay=3000)


def disconnect():
	current_meta = localinfo.get_meta2()
	linux.execute_and_wait("gksudo killall openvpn", timeout=60)
	linux.execute_and_wait("gksudo service networking restart", timeout=60)
	new_meta = localinfo.get_meta2()
	msg = "VPN DISCONNECTED! IP: {}=>{}; Region: {}=>{};".format(current_meta.ip, new_meta.ip, current_meta.ip_geo, new_meta.ip_geo)
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
	return linux.execute_and_wait(prepared_sh_script, timeout=10)


def start_vpn_service(domain_name, config, old_meta):
	pid = _process_openvpn_file(domain_name, config)
	current_ip = localinfo.get_ip()
	if old_meta.ip != current_ip:
		new_meta = localinfo.get_meta2()
		msg = "VPN CONNECTED! IP: {}; Region: {}; Dns: {}; DnsGeo: {};".format(new_meta.ip, new_meta.ipgeo, new_meta.dnsip, new_meta.dnsgeo)
	else:
		if pid_exists(pid):
			msg = "OPENVPN APPEARS TO BE STRUGGLING TO CONNECT! IP: {}; Region: {};".format(current_ip, old_meta.region)
		else:
			msg = "VPN FAILED TO CONNECT! IP: {}; Region: {};".format(current_ip, old_meta.region)
	linux.send_desktop_msg(msg, delay=3000)

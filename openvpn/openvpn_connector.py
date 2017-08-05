"""Launches vpn connection using NordVPN ovpn connection file. Supports passing optional arguments."""
import os
import subprocess


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


def start_vpn_service(domain_name, config, abort):
	# subprocess.Popen("content/vpn_up.sh")
	_process_openvpn_file(domain_name, config)
	abort["kill"] = True
	# subprocess.Popen("content/vpn_down.sh")

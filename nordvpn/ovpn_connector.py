import os
import subprocess


def _get_formatted_sh_script(ovpn_config_file_path):
	return "sudo openvpn --config {} --auth-user-pass auth.txt".format(
		ovpn_config_file_path
	)


def get_ovpn_file_path(domain_name):
	application_root = os.environ["APPLICATION_ROOT"]
	file_name = "{}.udp1194.ovpn".format(domain_name)
	return os.sep.join([application_root, "content", "ovpnfiles", file_name])


def process_ovpn_file(domain_name, config):
	absolute_path = get_ovpn_file_path(domain_name)
	prepared_sh_script = _get_formatted_sh_script(ovpn_config_file_path=absolute_path)
	print(prepared_sh_script)
	ps = subprocess.Popen(prepared_sh_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	ps.communicate()
	ps.wait()

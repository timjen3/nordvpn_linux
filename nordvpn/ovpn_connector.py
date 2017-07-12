import os
import subprocess


def _get_formatted_sh_script(absolute_ovpn_file_path, username, password):
	raw_text = "echo {2} | openvpn --config {0} --user {1} --askpass stdin"
	return raw_text.format(
		absolute_ovpn_file_path,
		username,
		password
	)


def get_ovpn_file_path(domain_name):
	application_root = os.environ["APPLICATION_ROOT"]
	file_name = "{}.udp1194.ovpn".format(domain_name)
	return os.sep.join([application_root, "content", "ovpnfiles", file_name])


def process_ovpn_file(domain_name, config):
	absolute_path = get_ovpn_file_path(domain_name)
	prepared_sh_script = _get_formatted_sh_script(absolute_ovpn_file_path=absolute_path, username=config["username"], password=config["password"])
	print(prepared_sh_script)
	ps = subprocess.Popen(prepared_sh_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	ps.communicate()
	ps.wait()

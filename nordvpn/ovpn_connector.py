import os
import subprocess


def _get_formatted_sh_script(root_dir, absolute_ovpn_file_path, username, password):
	sh_path = os.sep.join(["content", "boot_vpn.sh"])
	with open(sh_path, "rt") as fp:
		raw_text = fp.read()
		return raw_text.format(
			root_dir,
			absolute_ovpn_file_path,
			username,
			password
		)


def get_ovpn_file_path(domain_name):
	application_root = os.environ["APPLICATION_ROOT"]
	file_name = "{}.tcp443.ovpn".format(domain_name)
	return os.sep.join([application_root, "content", "ovpnfiles", file_name])


def process_ovpn_file(domain_name, root_path, config):
	root_dir = os.sep.join(root_path.split(os.sep)[0:-1])
	absolute_path = get_ovpn_file_path(domain_name)
	prepared_sh_script = _get_formatted_sh_script(root_dir=root_dir, absolute_ovpn_file_path=absolute_path, username=config["username"], password=config["password"])
	print(prepared_sh_script)
	ps = subprocess.Popen(prepared_sh_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	ps.communicate()
	ps.wait()

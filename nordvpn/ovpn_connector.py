from os import sep
import subprocess


def _get_formatted_sh_script(root_dir, relative_file_path, username, password):
	sh_path = sep.join(["content", "boot_vpn.sh"])
	with open(sh_path, "rt") as fp:
		raw_text = fp.read()
		return raw_text.format(
			root_dir,
			relative_file_path,
			username,
			password
		)


def get_ovpn_file_path(domain_name):
	file_name = "{}.tcp443.ovpn".format(domain_name)
	return sep.join(["ovpnfiles", file_name])


def process_ovpn_file(domain_name, root_path, config):
	root_dir = sep.join(root_path.split(sep)[0:-1])
	relative_path = get_ovpn_file_path(domain_name)
	prepared_sh_script = _get_formatted_sh_script(root_dir=root_dir, relative_file_path=relative_path, username=config["username"], password=config["password"])
	print(prepared_sh_script)
	ps = subprocess.Popen(prepared_sh_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	ps.communicate()
	ps.wait()

from tools import http_connector
from datetime import datetime
import pickle
import os


class NordVpnServerData:
	def __init__(self, config):
		self.config = config
		self.ovpn_file_dir = os.sep.join(["content", "ovpnfiles"])
		self.save_path = os.sep.join(["content", "persist.bin"])
		self.ensure_ovpn_files_exist()
		self.server_data = self.read()

	def read(self):
		if os.path.exists(self.save_path):
			with open(self.save_path, "rb") as fp:
				data = pickle.load(file=fp)
				return data
		else:
			return {"data": [], "date": None}

	def write(self, data):
		self.server_data = {
			"data": data,
			"date": datetime.utcnow()
		}
		with open(self.save_path, "wb") as fp:
			pickle.dump(self.server_data, file=fp)

	def ensure_ovpn_files_exist(self):
		# TODO: After x time passes re-download ovpn files.
		if not os.path.exists(self.ovpn_file_dir):
			os.makedirs(self.ovpn_file_dir)
			url = "https://api.nordvpn.com/files/zipv2"
			zip_file = http_connector.get_zip_file(url=url)
			zip_file.extractall(path=self.ovpn_file_dir)

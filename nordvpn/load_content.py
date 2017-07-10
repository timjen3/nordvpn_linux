from datetime import datetime
import pickle
import os


class NordVpnServerData:
	def __init__(self, config):
		self.config = config
		self.save_path = os.sep.join(["content", "persist.bin"])
		self.server_data = self.read()

	def read(self):
		if os.path.exists(self.save_path):
			with open(self.save_path, "rb") as fp:
				data = pickle.load(file=fp)
				data["date"] = datetime.strptime(data["date"], "%Y-%m-%d")
				return data

	def write(self, data):
		dump_data = {
			"data": data,
			"date": datetime.utcnow().strftime("%Y-%m-%d")
		}
		with open(self.save_path, "wb") as fp:
			pickle.dump(dump_data, file=fp)

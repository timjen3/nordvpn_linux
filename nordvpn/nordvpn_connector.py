from tools.http_connector import get_json
from tools.models import Server


class ServerManager:
	def __init__(self):
		self.servers = list()

	def load(self, servers):
		for server in servers:
			server_proper = Server()
			server_proper.domain = server["domain"]
			server_proper.country = server["country"]
			server_proper.latitude = server["location"]["lat"]
			server_proper.longitude = server["location"]["long"]
			server_proper.load = server["load"]
			self.servers.append(server_proper)


def servers(url):
	servers = get_json(url=url)
	sm = ServerManager()
	sm.load(servers=servers)
	return sm.servers

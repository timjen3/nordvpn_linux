from tools.http_connector import get_json
from tools.nordvpn_linux_models import Server
from nordvpn.load_content import NordVpnServerData
from datetime import datetime, timedelta
from tools import localinfo, filter_ranker
import logging


def should_refresh(last_refresh, refresh_interval=timedelta(hours=12)):
	logger = logging.getLogger(__name__)
	if last_refresh is None:
		return True
	time_to_refresh = last_refresh + refresh_interval
	refresh_needed = datetime.utcnow() > time_to_refresh
	logger.debug("Cached server data will {} used because it expires at: '{}'.".format(
		{True: "not be", False: "be"}[refresh_needed],
		time_to_refresh,
	))
	return refresh_needed


class ServerManager:
	def __init__(self, config):
		self.config = config
		self.locale_data = localinfo.get_meta()
		self.persistence = NordVpnServerData(config)
		self._filter_ranker = filter_ranker.ServerRanker(self.locale_data)

		self.refresh_server_data_if_needed()
		self._filter_ranker.load(self.persistence.server_data["data"], config["max_load"])

	@property
	def servers(self):
		while True:
			for server in self._filter_ranker.servers:
				yield server
				if self.refresh_server_data_if_needed():
					break  # Restart iterations b/c size changed.

	def refresh_server_data_if_needed(self):
		last_refresh = self.persistence.server_data["date"]
		if should_refresh(last_refresh):
			servers = get_json(url=self.config["nord_server_meta_url"])
			self._load(servers=servers)
			self._filter_ranker.load(self.persistence.server_data["data"], max_load=self.config["max_load"])
			return True
		return False

	def _load(self, servers):
		"""Loads servers into correct format."""
		self.persistence.server_data["data"] = list()
		servers_proper = list()
		for server in servers:
			server_proper = Server()
			server_proper.domain = server["domain"]
			server_proper.country = server["country"]
			server_proper.latitude = server["location"]["lat"]
			server_proper.longitude = server["location"]["long"]
			server_proper.load = server["load"]
			server_proper.features = server["features"]
			servers_proper.append(server_proper)
		self.persistence.write(servers_proper)

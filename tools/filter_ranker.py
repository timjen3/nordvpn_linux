from tools.coord_calc import haversine


def _has_category(server, values):
	for cat in values:
		if cat not in server.categories:
			return False
	return True


def _clean_for_matching(val):
	return str(val).replace(" ", "").upper()


class ServerRanker:
	"""Sorts and filters servers. Model structure can be found in nordvpn_linux_models."""
	def __init__(self, locale_meta):
		self.servers = []
		self.locale_info = locale_meta
		self.server_distance_classes = dict()
		self.server_load_classes = dict()

	def load(self, servers, config):
		"""
		Calculates distance of each server. Also enumerates distance for convenience.
		:param servers: A list of Server() defined by nordvpn_linux_models
		:param max_load: Maximum amount of load allowed when filtering servers.
		"""
		for s in servers:
			s.distance = haversine(coorda=(self.locale_info.longitude, self.locale_info.latitude), coordb=(s.longitude, s.latitude))
		distances = set([s.distance for s in servers])
		ordered_distances = sorted(distances)
		distance_classes = {d: i for i, d in enumerate(ordered_distances)}
		for s in servers:
			s.distance_class = distance_classes[s.distance]
		self.servers = servers
		self.sort()
		self.filter("load", lambda v: v < config["max_load"])
		for cat in config["required_categories"]:
			self.filter("categories", lambda v: cat in v)
		for sk in config["required_search_keywords"]:
			self.filter("search_keywords", lambda v: sk in v)

	def sort(self):
		"""Country will appear first if there is a match, then distance, lastly server load."""
		self.servers = sorted(self.servers, key=lambda s: s.load)
		self.servers = sorted(self.servers, key=lambda s: s.distance_class)
		self.servers = sorted(self.servers, key=lambda s: s.country == self.locale_info.country, reverse=True)

	def filter(self, key, fun):
		self.servers = [s for s in self.servers if fun(getattr(s, key))]

from tools.coord_calc import haversine


def _clean_for_matching(val):
	return str(val).replace(" ", "").upper()


class ServerRanker:
	"""Sorts and filters servers. Model structure can be found in nordvpn_linux_models."""
	def __init__(self, locale_meta):
		self.servers = []
		self.locale_info = locale_meta
		self.server_distance_classes = dict()
		self.server_load_classes = dict()

	def load(self, servers, max_load):
		"""
		Calculates distance of each server. Also enumerates distance and load for convenience.
		:param servers: A list of Server() defined by nordvpn_linux_models
		:param max_load: Maximum amount of load allowed when filtering servers.
		"""
		for s in servers:
			s.distance = haversine(coorda=(self.locale_info.latitude, self.locale_info.longitude), coordb=(s.latitude, s.longitude))
		distances = set([s.distance for s in servers])
		ordered_distances = sorted(distances)
		distance_classes = {d: i for i, d in enumerate(ordered_distances)}
		loads = set([s.load for s in servers])
		ordered_loads = sorted(loads)
		load_classes = {d: i for i, d in enumerate(ordered_loads)}
		for s in servers:
			s.distance_class = distance_classes[s.distance]
			s.load_class = load_classes[s.load]
		self.servers = servers
		self.sort()
		self.filter(max_load)

	def sort(self):
		"""Country will appear first if there is a match, then distance, lastly server load."""
		self.servers = sorted(self.servers, key=lambda s: s.load_class)
		self.servers = sorted(self.servers, key=lambda s: s.distance_class)
		self.servers = sorted(self.servers, key=lambda s: s.country == self.locale_info.country, reverse=True)

	def filter(self, max_load):
		self.servers = [s for s in self.servers if s.load < max_load]

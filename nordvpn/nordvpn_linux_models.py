class Server:
	def __init__(self, **kwargs):
		my_attributes = [
			"domain",
			"ip",
			"response_ms",
			"country",
			"latitude",
			"longitude",
			"distance",
			"distance_class",
			"load",
			"region",
			"zip",
			"features",
			"categories",
			"search_keywords",
		]
		for attribute in my_attributes:
			setattr(self, attribute, kwargs.get(attribute, None))
		load = str(kwargs.get("load", ""))
		if load.isdigit():
			self.load = int(load)
		else:
			self.load = 100

	@property
	def serializable(self):
		return {k: v for k, v in self.__dict__.items() if k[0] != "_"}


class LocaleInfo:
	def __init__(self, ip, **kwargs):
		self.ip = ip
		my_attributes = [
			"country",
			"zipcode",
			"latitude",
			"longitude",
			"region",
			"city",
			"isp"
		]
		for attribute in my_attributes:
			setattr(self, attribute, kwargs.get(attribute, None))

	@property
	def serializable(self):
		return {k: v for k, v in self.__dict__.items() if k[0] != "_"}


class LocaleInfo2:
	def __init__(self, **kwargs):
		my_attributes = [
			"ip",
			"ip_geo",
			"dns_ip",
			"dns_ip_geo",
		]
		for attribute in my_attributes:
			setattr(self, attribute, kwargs.get(attribute, None))

	@property
	def serializable(self):
		return {k: v for k, v in self.__dict__.items() if k[0] != "_"}

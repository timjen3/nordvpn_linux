class Server:
	def __init__(self, **kwargs):
		my_attributes = [
			"domain",
			"country",
			"latitude",
			"longitude",
			"distance",
			"distance_class",
			"load_class",
			"region",
			"zip"
		]
		for attribute in my_attributes:
			setattr(self, attribute, kwargs.get(attribute, None))
		load = str(kwargs.get("load", ""))
		if load.isdigit():
			self.load = int(load)
		else:
			self.load = 100


class LocaleInfo:
	def __init__(self, **kwargs):
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

from math import radians, cos, sin, asin, sqrt


def haversine(coorda, coordb):
	"""https://stackoverflow.com/a/15737218"""
	lon1, lat1, lon2, lat2 = map(radians, [coorda[0], coorda[1], coordb[0], coordb[1]])
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a))
	mi = round(3956.27036673 * c, 3)
	return "{} miles".format(mi)

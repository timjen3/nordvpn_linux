import subprocess
import os


def get_avg_ping(host):
	_num_pings = 5
	total_response_time = 0
	host = host.replace("https", "").replace("http", "").replace("://", "")
	p2 = {"nt": "-n", "posix": "-c"}
	ping = subprocess.Popen(["ping", p2[os.name], str(_num_pings), host], stdout=subprocess.PIPE)
	for line in ping.stdout.readlines():
		line_as_string = line.decode("utf-8")
		if "time=" in line_as_string and "ms" in line_as_string:
			response_time = line_as_string.split("time=")[1].split("ms")[0]
			total_response_time += float(response_time)
		elif "Time out" in line_as_string:
			total_response_time += 1000
		elif "could not find host" in line_as_string:
			total_response_time += 9999 * _num_pings
	ping.stdout.close()
	if total_response_time == 0:
		return 99999
	avg_response_time = float(total_response_time / _num_pings)
	return avg_response_time

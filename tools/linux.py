import subprocess
import os


"""https://stackoverflow.com/questions/568271/how-to-check-if-there-exists-a-process-with-a-given-pid-in-python"""
if os.name == 'posix':
	def pid_exists(pid):
		"""Check whether pid exists in the current process table."""
		import errno
		if pid < 0:
			return False
		try:
			os.kill(pid, 0)
		except OSError as e:
			return e.errno == errno.EPERM
		else:
			return True
elif os.name == 'nt':
	def pid_exists(pid):
		"""Dev was done on windows, so needed this to work on there also."""
		task_list = subprocess.Popen(["tasklist", "/FO", "CSV"], stdout=subprocess.PIPE)
		headers = task_list.stdout.readline().decode("utf-8")
		headers = [c for c in headers.split(",")]
		pid_col = [i for i, c in enumerate(headers) if c == '"PID"'][0]
		for line in task_list.stdout.readlines():
			_this_pid = int(line.decode("utf-8").replace('"', "").split(",")[pid_col])
			if _this_pid == pid:
				return True
		return False
else:
	def pid_exists(pid):
		raise NotImplementedError("Not implemented for '{}'".format(os.name))


def send_desktop_msg(msg_string, delay=0):
	"""
	:param msg_string: message to send to display
	:param delay: time to display message. 0 requires click to close.
	"""
	msg = 'notify-send "{}" -t {}'.format(msg_string, delay)
	os.popen(msg)


def execute_no_wait(command):
	try:
		sp = subprocess.Popen(command, shell=True)
	except:
		return -1
	return sp.pid


def execute_and_wait(command, timeout=5):
	try:
		sp = subprocess.Popen(command, shell=True)
		sp.communicate()
		sp.wait(timeout=timeout)
	except:
		return -1

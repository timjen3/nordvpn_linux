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
else:
	def pid_exists(pid):
		import ctypes
		kernel32 = ctypes.windll.kernel32
		SYNCHRONIZE = 0x100000
		process = kernel32.OpenProcess(SYNCHRONIZE, 0, pid)
		if process != 0:
			kernel32.CloseHandle(process)
			return True
		else:
			return False


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
		return 0
	return sp.pid


def execute_and_wait(command, timeout=5):
	try:
		sp = subprocess.Popen(command, shell=True)
	except:
		return 0
	sp.communicate()
	sp.wait(timeout=timeout)

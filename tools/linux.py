import subprocess
import os


def send_desktop_msg(msg_string, delay=0):
	"""
	:param msg_string: message to send to display
	:param delay: time to display message. 0 requires click to close.
	"""
	msg = 'notify-send "{}" -t {}'.format(msg_string, delay)
	os.popen(msg)


def execute_no_wait(command):
	sp = subprocess.Popen("gksudo {}".format(command))
	sp.communicate()
	return sp.pid


def execute_and_wait(command):
	sp = subprocess.Popen("gksudo {}".format(command))
	sp.communicate()
	sp.wait()

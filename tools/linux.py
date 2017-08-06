import os


def send_desktop_msg(msg_string, delay=0):
	"""
	:param msg_string: message to send to display
	:param delay: time to display message. 0 requires click to close.
	"""
	msg = 'notify-send "{}" -t {}'.format(msg_string, delay)
	os.popen(msg)

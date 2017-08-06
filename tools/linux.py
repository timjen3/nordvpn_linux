import os


def send_desktop_msg(msg_string):
	msg = 'notify-send "{}"'.format(msg_string)
	os.popen(msg)

import os


def send_desktop_msg(msg_string):
	safe_string = msg_string.replace("\n", ";").replace("\t", " ")
	msg = 'notify-send "{}"'.format(safe_string)
	os.popen(msg)
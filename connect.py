# TODO: Add a kill switch please!!!
from job_runner import *
import traceback
import logging
import json
import sys
import os


if __name__ == "__main__":
	print("Init bootstrapping process...")
	from gui.simple_gui import start_gui
	try:
		config_path = os.sep.join(["content", "tool.json"])
		with open(config_path, "r") as fp:
			tool_config = json.loads(fp.read())

		app_log_dir = tool_config.get("application_log_dir", "")
		application_log_path = "{}{}".format(app_log_dir, "application.log")

	except:
		print("Failed to bootstrap!\n{}".format(traceback.format_exc()))
		sys.exit(1)

	print("Init logger...")
	try:
		logging.basicConfig(
			level=logging.DEBUG,
			format='%(asctime)s %(levelname)s {%(pathname)s:%(lineno)d} %(message)s',
			handlers=[logging.StreamHandler(), logging.FileHandler(filename=application_log_path, mode="w")],
		)
		logger = logging.getLogger(__name__)
	except:
		print("Failed to init logging!\n{}".format(traceback.format_exc()))
		sys.exit(2)

	logger.debug("Application bootstrapped. Starting GUI.")
	try:
		locale_info = get_meta()
		local_msg = "IP:{}\nREGION:{}".format(locale_info.ip, locale_info.region)
		start_gui(start_fun=connect_vpn, stop_fun=disconnect_function, alive_fun=check_alive, locale_info=local_msg)
	except:
		logger.critical("Program crashed!\n{}".format(traceback.format_exc()))

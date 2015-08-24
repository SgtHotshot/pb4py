import logging
import logging.config

class Logs(object):
	@staticmethod
	def getLogger(name):
		log_formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

		handler = logging.StreamHandler()
		handler.setLevel(logging.DEBUG)
		handler.setFormatter(log_formatter)

		logger = logging.getLogger(name)
		logger.setLevel(logging.DEBUG)

		logger.addHandler(handler)

		return logger


import logging
import logging.config

class Logs(object):
	handle = None

	def getLogger(self, name):
		if not self.handle:
			logFormatter = logging.Formatter(fmt='%(asctime)s - %(module)s - %(levelname)s - %(message)s')
			
			handler = logging.StreamHandler()
			handler.setLevel(logging.DEBUG)
			handler.setFormatter(logFormatter)
		
			logger = logging.getLogger(name)
			logger.setLevel(logging.DEBUG)
			
			logger.addHandler(handler)
			self.handle = handler
		else:
			logger = logging.getLogger(name)
		
		return logger
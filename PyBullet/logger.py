import logging
import logging.config

def getLogger(name):
	logFormatter = logging.Formatter(fmt='%(asctime)s - %(module)s - %(levelname)s - %(message)s')
	
	handler = logging.StreamHandler()
	handler.setFormatter(logFormatter)
	
	logger = logging.getLogger(name)
	
	logger.addHandler(handler)
	
	return logger
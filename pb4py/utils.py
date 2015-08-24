def log_and_raise(self, message, exception_type = Exception):
	self.logger.error(message)
	raise exception_type(message)


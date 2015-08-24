def log_and_raise(logger, message, exception_type = Exception):
	logger.error(message)

	raise exception_type(message)


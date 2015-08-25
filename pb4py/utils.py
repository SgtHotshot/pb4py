import pb4py.exceptions

def log_and_raise(logger, message, exception_type = pb4py.exceptions.PB4PyException):
	logger.error(message)

	raise exception_type(message)


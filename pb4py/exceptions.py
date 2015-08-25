class PB4PyException(Exception):
	"""
	A simple exception wrapper to make it easier to pin point where things
	fail.
	"""

class PB4PyConfigurationException(PB4PyException):
	"""
	There was something wrong with the PB4Py configuration/settings.
	"""

class PB4PyAPIException(PB4PyException):
	"""
	There was something wrong when trying to talk to the PushBullet API.
	"""


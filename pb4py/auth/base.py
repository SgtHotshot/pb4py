import abc

import requests

from pb4py import utils
from pb4py.logger import Logs

class Authenticator(object):
	"""
	Base authentication mechanism
	"""

	__metaclass__ = abc.ABCMeta

	def __init__(self, settings):
		"""
		Create the authenticator with the given settings
		"""

		self.logger   = Logs.getLogger('PyBullet:Request')
		self.settings = settings

	@abc.abstractmethod
	def get_request_auth(self):
		"""
		Get the authentication information for this request.
		"""


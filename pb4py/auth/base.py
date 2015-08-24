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

	def send_request(self, url, method, skip_auth = False, **kwargs):
		"""
		Send authenticated request
		"""

		auth = self.get_request_auth() if not skip_auth else None

		resp = requests.request(method, url, auth = auth, **kwargs)
		if resp.status_code < 200 and resp.status_code >= 300:
			utils.log_and_raise('Bad status code of {} returned'.format(resp.status_code), IOError)

		ret = resp.json() if resp.status_code != 204 else None

		return ret


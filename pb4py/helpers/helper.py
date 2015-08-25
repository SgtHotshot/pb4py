import abc
import requests

from pb4py import exceptions, utils

# Try and import urlparse. This may fail based on the version of Python that is
# on the system. We do provide a fallback option, however.
try:
	import urlparse
except ImportError:
	# pylint: disable=import-error, no-name-in-module
	import urllib.parse
	urlparse = urllib.parse
	# pylint: enable=import-error, no-name-in-module

class Helper(object):
	__metaclass__ = abc.ABCMeta

	API_ROOT    = 'https://api.pushbullet.com'
	API_VERSION = '/v2'

	def _send_request(self, url, method, url_kwargs = {}, skip_auth = False, **kwargs):
		url_parts = urlparse.urlparse(Helper.API_ROOT)

		url = urlparse.urlunparse(
			(
				url_parts.scheme,
				url_parts.netloc,
				url.format(**url_kwargs),
				'',
				'',
				'',
			)
		)

		auth = self.auth.get_request_auth() if not skip_auth else None

		resp = requests.request(method, url, auth = auth, **kwargs)
		if resp.status_code < 200 and resp.status_code >= 300:
			utils.log_and_raise(
				self.logger,
				'Bad status code of {} returned'.format(resp.status_code),
				exceptions.PB4PyAPIException,
			)

		ret = resp.json() if resp.status_code != 204 else None

		return ret

	@staticmethod
	def _filter_inactive(elements):
		return [elem for elem in elements if elem['active']]


from pb4py.helpers import Helper

import json

class MeHelper(Helper):
	URL_ME = Helper.API_VERSION + '/users/me'

	def me(self):
		"""
		Get information about the current user
		"""

		return self._send_request(MeHelper.URL_ME, 'GET')

	def update_me(self, **kwargs):
		"""
		Update current user preferences
		"""

		return self._send_request(
			MeHelper.URL_ME,
			'POST',
			headers = {'content-type': 'application/json'},
			data    = json.dumps(kwargs),
		)


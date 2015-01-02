from . import base

# pylint: disable=no-init

class BasicAuthenticator(base.Authenticator):
	"""
	Basic authenticator for PushBullet that logs the client in
	as the specified user using their access token. The access
	token can be retrieved from the account settings page. Use
	of the access token gives the client full access to the user's
	account.
	"""

	def get_request_auth(self):
		return (self.access_token, '')

	@property
	def access_token(self):
		"""
		Get the user's access token
		"""

		return self.settings['access_token']


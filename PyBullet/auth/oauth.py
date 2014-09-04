from . import base

# pylint: disable=no-init

class OAuthAuthenticationError(Exception):
	"""
	Authentication error when using OAuth. Usually
	this means that the user hasn't granted
	the application permission.
	"""

class OAuthAuthenticator(base.Authenticator):
	"""
	Authenticator that uses OAuth to work on a users behalf.
	The application must be registered with PushBullet and
	the client_id and client_secret set in the configuration.
	When a request is made for a user they must have granted
	the app permission to use their information. This is the
	preferred way to do things.
	"""

	def get_request_auth(self):
		return (self.access_token, '')

	@property
	def access_token(self):
		"""
		Get the user's access token for this application.
		"""

		if 'access_token' not in self.settings:
			# pylint: disable=line-too-long
			try:
				raise OAuthAuthenticationError(
					'User access token unkown. Grant the application permission by going to {} and then set the access_token with the value that is returned'.format(
						self.oauth_grant_url,
					),
				)
			except OAuthAuthenticationError:
				self.logger(
					'User access token unkown. Grant the application permission by going to {} and then set the access_token with the value that is returned'.format(
						self.oauth_grant_url,
					),
				)
				raise
			# pylint: enable=line-too-long

		return self.settings['access_token']

	@property
	def client_id(self):
		"""
		Get the application's client ID
		"""

		return self.settings['client_id']

	@property
	def client_secret(self):
		"""
		Get the application's client secret
		"""

		return self.settings['client_secret']

	@property
	def request_uri(self):
		"""
		Get the request URI to use to request permission to
		operate as a user.
		"""

		return self.settings['request_uri']

	@property
	def oauth_grant_url(self):
		"""
		The URL to use to grant the application permission to
		operate as a user.
		"""

		# pylint: disable=line-too-long
		return 'https://www.pushbullet.com/authorize?client_id={}&request_uri={}&response_type=token'.format(
			self.client_id,
			self.request_uri,
		)
		# pylint: enable=line-too-long


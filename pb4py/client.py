from pb4py import auth, exceptions, helpers, utils
from pb4py.logger import Logs

import json
import os.path

class Client(
		helpers.ChannelHelper,
		helpers.ContactHelper,
		helpers.DeviceHelper,
		helpers.MeHelper,
		helpers.PushHelper,
		helpers.SubscriptionHelper):
	"""
	PushBullet client for Python.
	"""

	GLOBAL_SETTINGS_FILE = os.path.expanduser('~/.pb4pyrc')

	def __init__(self, settings = None):
		"""
		Creates a client based off of the given settings. The settings parameter
		can be a string that points to a JSON file or it can be dictionary of
		setting values. These settings override the "Global settings" that are
		set per user via the GLOBAL_SETTINGS_FILE.
		"""

		self.logger = Logs.getLogger('PB4Py')

		if not os.path.exists(Client.GLOBAL_SETTINGS_FILE) and not settings:
			utils.log_and_raise(
				self.logger,
				'No settings given',
				exceptions.PB4PyConfigurationException,
			)

		if os.path.exists(Client.GLOBAL_SETTINGS_FILE):
			self.settings = Client._load_config()
			self.logger.debug('Config file loaded')
		else:
			self.settings = {}

		if settings:
			if isinstance(settings, str):
				settings = Client._load_config(settings)
				self.logger.info('Parameter config loaded')

			self.settings.update(settings)

		self.auth = self._get_auth_module(self.settings.get('auth', None))

	def _get_auth_module(self, auth_settings):
		if not auth_settings:
			utils.log_and_raise(
				self.logger,
				'No authentication settings found',
				exceptions.PB4PyConfigurationException,
			)

		if auth_settings['type'] == 'basic':
			self.logger.debug('Selected Basic Authenticator')

			return auth.BasicAuthenticator(auth_settings)
		elif auth_settings['type'] == 'oauth':
			self.logger.debug('Selected OAuth Authenticator')

			return auth.OAuthAuthenticator(auth_settings)
		else:
			utils.log_and_raise(
				self.logger,
				'Invalid authentication scheme given. Must be basic or oauth',
				exceptions.PB4PyConfigurationException,
			)

	@staticmethod
	def _load_config(settings = None):
		"""
		Load the configuration file.
		"""

		settings = settings or Client.GLOBAL_SETTINGS_FILE

		with open(settings, 'r') as fh:
			return json.load(fh)


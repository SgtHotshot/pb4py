from pb4py import auth, exceptions, utils
from pb4py.logger import Logs

import json
import mimetypes
import os
import os.path
import requests

# Try and import urlparse. This may fail based on the version of Python that is
# on the system. We do provide a fallback option, however.
try:
	import urlparse
except ImportError:
	# pylint: disable=import-error, no-name-in-module
	import urllib.parse
	urlparse = urllib.parse
	# pylint: enable=import-error, no-name-in-module

class Client(object):
	"""
	PushBullet client for Python.
	"""

	GLOBAL_SETTINGS_FILE = os.path.expanduser('~/.pb4pyrc')

	API_ROOT                = 'https://api.pushbullet.com'
	API_VERSION             = '/v2'
	URL_CONTACTS_LIST       = API_VERSION + '/contacts'
	URL_CONTACTS_CREATE     = URL_CONTACTS_LIST
	URL_CONTACTS_UPDATE     = URL_CONTACTS_LIST + '/{contact}'
	URL_CONTACTS_DELETE     = URL_CONTACTS_UPDATE
	URL_DEVICE_LIST         = API_VERSION + '/devices'
	URL_DEVICE_CREATE       = URL_DEVICE_LIST
	URL_DEVICE_UPDATE       = URL_DEVICE_LIST + '/{device}'
	URL_DEVICE_DELETE       = URL_DEVICE_UPDATE
	URL_ME                  = API_VERSION + '/users/me'
	URL_PUSH_SEND           = API_VERSION + '/pushes'
	URL_PUSH_HISTORY        = URL_PUSH_SEND
	URL_PUSH_DISMISS        = URL_PUSH_SEND + '/{push}'
	URL_PUSH_DELETE         = URL_PUSH_DISMISS
	URL_FILE_UPLOAD         = API_VERSION + '/upload-request'
	URL_CHANNEL_INFO        = API_VERSION + '/channel-info'
	URL_SUBSCRIPTION_LIST   = API_VERSION + '/subscriptions'
	URL_SUBSCRIPTION_CREATE = URL_SUBSCRIPTION_LIST
	URL_SUBSCRIPTION_DELETE = URL_SUBSCRIPTION_LIST + '/{channel}'
	
	MAX_FILE_SIZE = 25000000
	MB_DIVIDE     = (1024.0 * 1024.0)

	PUSH_TYPES = [
		'file',
		'link',
		'note',
	]

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

	def devices(self, exclude_inactive = True):
		"""
		List devices.
		"""

		resp = self._send_request(Client.URL_DEVICE_LIST, 'GET')

		devices = resp['devices']

		return devices if not exclude_inactive else Client._filter_inactive(devices)

	def create_device(self, name, device_type):
		"""
		Create a device.
		"""

		resp = self.auth.send_request(
			Client.URL_DEVICE_CREATE,
			'POST',
			data = {
				'type': device_type,
				'nickname': name,
			},
		)

		return resp

	def update_device(self, device_iden, **kwargs):
		"""
		Update an existing device. kwargs gives the values that will be updated.
		"""

		return self._send_request(
			Client.URL_DEVICE_UPDATE + '/' + device_iden,
			'POST',
			url_kwargs = {'device': device_iden},
			data       = kwargs,
		)

	def delete_device(self, device_iden):
		"""
		Delete the given device.
		"""

		self._send_request(
			Client.URL_DEVICE_DELETE,
			'DELETE',
			url_kwargs = {'device': device_iden},
		)

	def push(self, push_type, **kwargs):
		"""
		Push to a specific device, all devices, or a user. Pushes come in several type
		and each type requires different parameters. These types and their
		parameters are:

		push_type = note
			* title - note's title
			* body  - note's message

		push_type = link
			* title - the link's title
			* url   - the url to open
			* body  - optional message

		push_type = file
			* file_name - the name of the file
			* file_type - the MIME type of the file
			* file_url  - the url where the file can be downloaded
			* body      - message to with the file

		All push types also take a device_iden or email parameter to push to a
		device or user. If device_iden is not given the push goes to all devices.

		To send a push to a channel use the parameter channel_tag.

		To push a file you must first upload it using the upload_file method.
		"""

		if push_type not in Client.PUSH_TYPES:
			utils.log_and_raise(
				self.logger,
				'Invalid push type {}'.format(push_type),
				exceptions.PB4PyException
			)

		kwargs['type'] = push_type

		return self._send_request(Client.URL_PUSH_SEND, 'POST', data = kwargs)

	def push_history(self, modified_timestamp = 0, exclude_inactive = True):
		"""
		Get all the pushes that were created/modified after the given
		UNIX timestamp.
		"""

		return self._send_request(
			Client.URL_PUSH_HISTORY,
			'GET',
			params = {
				'active':        'true' if exclude_inactive else 'false',
				'modified_after': modified_timestamp,
			},
		)['pushes']

	def dismiss_push(self, push_iden):
		"""
		Dismiss a push
		"""

		return self._send_request(
			Client.URL_PUSH_DISMISS,
			'POST',
			url_kwargs = {'push': push_iden},
			data       = {'dismissed': 'true'},
		)

	def delete_push(self, push_iden):
		"""
		Delete a push
		"""

		self._send_request(
			Client.URL_PUSH_DELETE,
			'DELETE',
			url_kwargs = {'push': push_iden},
		)

	def contacts(self, exclude_inactive = True):
		"""
		Get contacts
		"""

		contacts = self._send_request(
			Client.URL_CONTACTS_LIST,
			'GET',
		)['contacts']

		return contacts if not exclude_inactive else Client._filter_inactive(contacts)

	def create_contact(self, name, email):
		"""
		Create a new contact
		"""

		return self._send_request(
			Client.URL_CONTACTS_CREATE,
			'POST',
			data = {'name': name, 'email': email},
		)

	def update_contact(self, contact_iden, **kwargs):
		"""
		Update contact information
		"""

		return self._send_request(
			Client.URL_CONTACTS_UPDATE,
			'POST',
			url_kwargs = {'contact': contact_iden},
			data       = kwargs,
		)

	def delete_contact(self, contact_iden):
		"""
		Delete contact
		"""

		self._send_request(
			Client.URL_CONTACTS_DELETE,
			'DELETE',
			url_kwargs = {'contact': contact_iden}
		)

	def me(self):
		"""
		Get information about the current user
		"""

		return self._send_request(Client.URL_ME, 'GET')

	def update_me(self, **kwargs):
		"""
		Update current user preferences
		"""

		return self._send_request(
			Client.URL_ME,
			'POST',
			headers = {'content-type': 'application/json'},
			data    = json.dumps(kwargs),
		)

	def upload_file(self, input_file, filename = None, file_type = None):
		"""
		Upload a file. The inputfile parameter can be a file path string
		or a file handle. If you give a file handle you can override the
		filename that is sent to PushBullet. We try to guess the MIME type
		of the file but you can override that as well.
		"""

		if isinstance(input_file, str) and filename is None:
			filename = os.path.basename(input_file)

		we_opened_the_file = not isinstance(input_file, str)

		file_handle = open(input_file, 'rb') if isinstance(input_file, str) else input_file
		name        = filename or file_handle.name
		mime_type   = file_type or mimetypes.guess_type(name)

		size     = os.fstat(file_handle.fileno()).st_size
		fileSize = str(size / Client.MB_DIVIDE)
		if size <= Client.MAX_FILE_SIZE:
			self.logger.debug("File is: " + fileSize + "MB")
		else:
			self.logger.debug("File was bigger than 25mb.  It was: " + fileSize + "MB")
			return None

		resp = self._send_request(
			Client.URL_FILE_UPLOAD,
			'POST',
			data = {'file_name': name, 'file_type': mime_type}
		)

		self._send_request(
			resp['upload_url'],
			'POST',
			skip_auth = True,
			data      = resp['data'],
			files     = {
				'file': file_handle,
			},
		)

		if we_opened_the_file:
			file_handle.close()

		return resp

	def subscriptions(self, exclude_inactive = True):
		"""
		List Subscriptions
		"""

		subscriptions = self._send_request(Client.URL_SUBSCRIPTION_LIST, 'GET')['subscriptions']

		return subscriptions if not exclude_inactive else Client._filter_inactive(subscriptions)

	def subscribe_to_channel(self, channel_tag):
		"""
		Subscribe to a channel
		"""

		return self._send_request(
			Client.URL_SUBSCRIPTION_CREATE,
			'POST',
			data = {'channel_tag': channel_tag},
		)

	def get_channel_info(self, channel_tag):
		"""
		Get a Channel's Info
		"""

		return self._send_request(
			Client.URL_CHANNEL_INFO,
			'GET',
			params = {'tag': channel_tag},
		)

	def unsubscribe_to_channel(self, channel_id):
		"""
		UnSubscribe to a channel
		"""

		return self._send_request(
			Client.URL_SUBSCRIPTION_DELETE,
			'DELETE',
			url_kwargs = {'channel': channel_id},
		)

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

	def _send_request(self, url, method, url_kwargs = {}, skip_auth = False, **kwargs):
		url_parts = urlparse.urlparse(Client.API_ROOT)

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
	def _load_config(settings = None):
		"""
		Load the configuration file.
		"""

		settings = settings or Client.GLOBAL_SETTINGS_FILE

		with open(settings, 'r') as fh:
			return json.load(fh)

	@staticmethod
	def _filter_inactive(elements):
		return [elem for elem in elements if elem['active']]


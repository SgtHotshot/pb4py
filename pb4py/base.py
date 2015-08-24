from pb4py import auth, utils
from pb4py.logger import Logs

import json
import mimetypes
import os
import os.path

class Client(object):
	"""
	PushBullet client for Python.
	"""

	GLOBAL_SETTINGS_FILE = os.path.expanduser('~/.pb4pyrc')

	BASE_URL         = 'https://api.pushbullet.com/v2'
	CONTACTS_URL     = BASE_URL + '/contacts'
	DEVICE_URL       = BASE_URL + '/devices'
	ME_URL           = BASE_URL + '/users/me'
	PUSH_URL         = BASE_URL + '/pushes'
	UPLOAD_URL       = BASE_URL + '/upload-request'
	SUBSCRIPTION_URL = BASE_URL + '/subscriptions'
	CHANNEL_URL      = BASE_URL + '/channel-info'
	
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
			self.logger.error('No settings given')
			raise Exception('No settings given')

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

		resp = self.auth.send_request(Client.DEVICE_URL, 'GET')

		devices = resp['devices']

		return devices if not exclude_inactive else Client._filter_inactive(devices)

	def create_device(self, name, device_type):
		"""
		Create a device.
		"""

		resp = self.auth.send_request(
			Client.DEVICE_URL,
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

		return self.auth.send_request(
			Client.DEVICE_URL + '/' + device_iden,
			'POST',
			data = kwargs,
		)

	def delete_device(self, device_iden):
		"""
		Delete the given device.
		"""

		self.auth.send_request(Client.DEVICE_URL + '/' + device_iden, 'DELETE')

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
			raise ValueError('Invalid push type {}'.format(push_type))

		kwargs['type'] = push_type

		return self.auth.send_request(Client.PUSH_URL, 'POST', data = kwargs)

	def push_history(self, modified_timestamp = 0, exclude_inactive = True):
		"""
		Get all the pushes that were created/modified after the given
		UNIX timestamp.
		"""

		return self.auth.send_request(
			Client.PUSH_URL,
			'GET',
			params = {
				'active': 'true' if exclude_inactive else 'false',
				'modified_after': modified_timestamp,
			},
		)['pushes']

	def dismiss_push(self, push_iden):
		"""
		Dismiss a push
		"""

		return self.auth.send_request(
			Client.PUSH_URL + '/' + push_iden,
			'POST',
			data = {'dismissed': 'true'}
		)

	def delete_push(self, push_iden):
		"""
		Delete a push
		"""

		self.auth.send_request(
			Client.PUSH_URL + '/' + push_iden,
			'DELETE',
		)

	def contacts(self, exclude_inactive = True):
		"""
		Get contacts
		"""

		contacts = self.auth.send_request(
			Client.CONTACTS_URL,
			'GET',
		)['contacts']

		return contacts if not exclude_inactive else Client._filter_inactive(contacts)

	def create_contact(self, name, email):
		"""
		Create a new contact
		"""

		return self.auth.send_request(
			Client.CONTACTS_URL,
			'POST',
			data = {'name': name, 'email': email},
		)

	def update_contact(self, contact_iden, **kwargs):
		"""
		Update contact information
		"""

		return self.auth.send_request(
			Client.CONTACTS_URL + '/' + contact_iden,
			'POST',
			data = kwargs,
		)

	def delete_contact(self, contact_iden):
		"""
		Delete contact
		"""

		self.auth.send_request(
			Client.CONTACTS_URL + '/' + contact_iden,
			'DELETE',
		)

	def me(self):
		"""
		Get information about the current user
		"""

		return self.auth.send_request(Client.ME_URL, 'GET')

	def update_me(self, **kwargs):
		"""
		Update current user preferences
		"""

		return self.auth.send_request(
			Client.ME_URL,
			'POST',
			headers = {'content-type': 'application/json'},
			data = json.dumps(kwargs),
		)

	def upload_file(self, inputfile, filename = None, file_type = None):
		"""
		Upload a file. The inputfile parameter can be a file path string
		or a file handle. If you give a file handle you can override the
		filename that is sent to PushBullet. We try to guess the MIME type
		of the file but you can override that as well.
		"""

		if isinstance(inputfile, str) and filename is None:
			filename = os.path.basename(inputfile)

		file_handle = open(inputfile, 'rb') if isinstance(inputfile, str) else inputfile
		name        = filename or file_handle.name
		mime_type   = file_type or mimetypes.guess_type(name)

		if isinstance(inputfile, str):
			size = str(os.path.getsize(inputfile)/Client.MB_DIVIDE)
			if os.path.getsize(inputfile) <= Client.MAX_FILE_SIZE:	
				self.logger.debug("File is: " + size + "MB")
			else:
				self.logger.debug("File was bigger than 25mb.  It was: " + size + "MB")
				return None
		else:
			self.logger.debug("Was a File Handle not a file path")
			size = os.fstat(file_handle.fileno()).st_size
			fileSize = str(size/Client.MB_DIVIDE)
			if size <= Client.MAX_FILE_SIZE:
				self.logger.debug("File is: " + fileSize + "MB")
			else:
				self.logger.debug("File was bigger than 25mb.  It was: " + fileSize + "MB")
				return None

		resp = self.auth.send_request(
			Client.UPLOAD_URL,
			'POST',
			data = {'file_name': name, 'file_type': mime_type}
		)

		self.auth.send_request(
			resp['upload_url'],
			'POST',
			skip_auth = True,
			data      = resp['data'],
			files     = {
				'file': file_handle,
			},
		)

		return resp

	def subscribe_to_channel(self, channel_tag):
		"""
			Subscribe to a channel
		"""

		return self.auth.send_request(
			Client.SUBSCRIPTION_URL,
			'POST',
			data = {'channel_tag': channel_tag}
		)

	def unsubscribe_to_channel(self, channel_id):
		"""
			UnSubscribe to a channel
		"""

		return self.auth.send_request(
			Client.SUBSCRIPTION_URL + '/' + channel_id,
			'DELETE',
		)

	def get_channel_info(self, channel_tag):
		"""
			Get a Channel's Info
		"""

		return self.auth.send_request(
			Client.CHANNEL_URL,
			'GET',
			params = {'tag': channel_tag},
		)

	def list_subscriptions(self):
		"""
			List Subscriptions
		"""

		return self.auth.send_request(Client.SUBSCRIPTION_URL,'GET')

	def _get_auth_module(self, auth_settings):
		if not auth_settings:
			utils.log_and_raise(self.logger, 'No authentication settings found')

		if auth_settings['type'] == 'basic':
			self.logger.info('Selected Basic Authenticator')

			return auth.BasicAuthenticator(auth_settings)
		elif auth_settings['type'] == 'oauth':
			self.logger.info('Selected OAuth Authenticator')

			return auth.OAuthAuthenticator(auth_settings)
		else:
			utils.log_and_raise(
				self.logger,
				'Invalid authentication scheme given. Must be basic or oauth',
			)

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


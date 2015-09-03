from pb4py import exceptions, utils
from pb4py.helpers import Helper

class PushHelper(Helper):
	URL_PUSH_SEND    = Helper.API_VERSION + '/pushes'
	URL_PUSH_HISTORY = URL_PUSH_SEND
	URL_PUSH_DISMISS = URL_PUSH_SEND + '/{push}'
	URL_PUSH_DELETE  = URL_PUSH_DISMISS
	URL_FILE_UPLOAD  = Helper.API_VERSION + '/upload-request'

	MAX_FILE_SIZE = 25000000
	MB_DIVIDE     = (1024.0 * 1024.0)

	PUSH_TYPES = [
		'file',
		'link',
		'note',
	]

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

		if push_type not in PushHelper.PUSH_TYPES:
			utils.log_and_raise(
				self.logger,
				'Invalid push type {}'.format(push_type),
				exceptions.PB4PyException
			)

		kwargs['type'] = push_type

		return self._send_request(PushHelper.URL_PUSH_SEND, 'POST', data = kwargs)

	def push_history(self, modified_timestamp = 0, exclude_inactive = True):
		"""
		Get all the pushes that were created/modified after the given
		UNIX timestamp.
		"""

		return self._send_request(
			PushHelper.URL_PUSH_HISTORY,
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
			PushHelper.URL_PUSH_DISMISS,
			'POST',
			url_kwargs = {'push': push_iden},
			data       = {'dismissed': 'true'},
		)

	def delete_push(self, push_iden):
		"""
		Delete a push
		"""

		self._send_request(
			PushHelper.URL_PUSH_DELETE,
			'DELETE',
			url_kwargs = {'push': push_iden},
		)


from pb4py.helpers import Helper

class DeviceHelper(Helper):
	URL_DEVICE_LIST   = Helper.API_VERSION + '/devices'
	URL_DEVICE_CREATE = URL_DEVICE_LIST
	URL_DEVICE_UPDATE = URL_DEVICE_LIST + '/{device}'
	URL_DEVICE_DELETE = URL_DEVICE_UPDATE

	def devices(self, exclude_inactive = True):
		"""
		List devices.
		"""

		resp = self._send_request(DeviceHelper.URL_DEVICE_LIST, 'GET')

		devices = resp['devices']

		return devices if not exclude_inactive else Helper._filter_inactive(devices)

	def create_device(self, name, device_type):
		"""
		Create a device.
		"""

		resp = self.auth.send_request(
			DeviceHelper.URL_DEVICE_CREATE,
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
			DeviceHelper.URL_DEVICE_UPDATE,
			'POST',
			url_kwargs = {'device': device_iden},
			data       = kwargs,
		)

	def delete_device(self, device_iden):
		"""
		Delete the given device.
		"""

		self._send_request(
			DeviceHelper.URL_DEVICE_DELETE,
			'DELETE',
			url_kwargs = {'device': device_iden},
		)


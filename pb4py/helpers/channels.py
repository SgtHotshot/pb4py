from pb4py.helpers import Helper

class ChannelHelper(Helper):
	URL_CHANNEL_INFO = Helper.API_VERSION + '/channel-info'

	def get_channel_info(self, channel_tag):
		"""
		Get a Channel's Info
		"""

		return self._send_request(
			ChannelHelper.URL_CHANNEL_INFO,
			'GET',
			params = {'tag': channel_tag},
		)


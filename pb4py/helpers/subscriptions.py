from pb4py.helpers import Helper

class SubscriptionHelper(Helper):
	URL_SUBSCRIPTION_LIST   = Helper.API_VERSION + '/subscriptions'
	URL_SUBSCRIPTION_CREATE = URL_SUBSCRIPTION_LIST
	URL_SUBSCRIPTION_DELETE = URL_SUBSCRIPTION_LIST + '/{channel}'

	def subscriptions(self, exclude_inactive = True):
		"""
		List Subscriptions
		"""

		subscriptions = self._send_request(
			SubscriptionHelper.URL_SUBSCRIPTION_LIST,
			'GET',
		)['subscriptions']

		return subscriptions if not exclude_inactive else Helper._filter_inactive(subscriptions)

	def subscribe_to_channel(self, channel_tag):
		"""
		Subscribe to a channel
		"""

		return self._send_request(
			SubscriptionHelper.URL_SUBSCRIPTION_CREATE,
			'POST',
			data = {'channel_tag': channel_tag},
		)

	def unsubscribe_to_channel(self, channel_id):
		"""
		UnSubscribe to a channel
		"""

		return self._send_request(
			SubscriptionHelper.URL_SUBSCRIPTION_DELETE,
			'DELETE',
			url_kwargs = {'channel': channel_id},
		)


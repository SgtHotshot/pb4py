from pb4py.helpers import Helper

class ContactHelper(Helper):
	URL_CONTACTS_LIST   = Helper.API_VERSION + '/contacts'
	URL_CONTACTS_CREATE = URL_CONTACTS_LIST
	URL_CONTACTS_UPDATE = URL_CONTACTS_LIST + '/{contact}'
	URL_CONTACTS_DELETE = URL_CONTACTS_UPDATE

	def contacts(self, exclude_inactive = True):
		"""
		Get contacts
		"""

		contacts = self._send_request(
			ContactHelper.URL_CONTACTS_LIST,
			'GET',
		)['contacts']

		return contacts if not exclude_inactive else Helper._filter_inactive(contacts)

	def create_contact(self, name, email):
		"""
		Create a new contact
		"""

		return self._send_request(
			ContactHelper.URL_CONTACTS_CREATE,
			'POST',
			data = {'name': name, 'email': email},
		)

	def update_contact(self, contact_iden, **kwargs):
		"""
		Update contact information
		"""

		return self._send_request(
			ContactHelper.URL_CONTACTS_UPDATE,
			'POST',
			url_kwargs = {'contact': contact_iden},
			data       = kwargs,
		)

	def delete_contact(self, contact_iden):
		"""
		Delete contact
		"""

		self._send_request(
			ContactHelper.URL_CONTACTS_DELETE,
			'DELETE',
			url_kwargs = {'contact': contact_iden}
		)


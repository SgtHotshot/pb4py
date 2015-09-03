#!/usr/bin/env python

from __future__ import print_function

import argparse
import json
import sys
import tabulate

import pb4py
import pb4py.exceptions



def add_device_commands(parsers):
	device_parsers = parsers.add_subparsers()

	device_parsers.add_parser(
		'list',
		help = 'List all devices.',
	).set_defaults(func = command_devices_list)



	create_device = device_parsers.add_parser(
		'create',
		help = 'Create a new PushBullet device.',
	)

	create_device.add_argument(
		'name',
		type = str,
		help = 'The name of the device',
	)

	create_device.add_argument(
		'device_type',
		type = str,
		help = 'The type of device (ex: Windows, phone, etc)',
	)

	create_device.set_defaults(func = command_devices_create)



	update_device = device_parsers.add_parser(
		'update',
		help = 'Update an existing PushBullet device.',
	)

	update_device.add_argument(
		'iden',
		type = str,
		help = 'The ID of the device',
	)

	update_device.add_argument(
		'--nickname',
		type    = str,
		default = None,
		help    = 'Set the device nickname',
	)

	update_device.add_argument(
		'--device_type',
		dest    = 'type',
		type    = str,
		default = None,
		help    = 'Set the device type',
	)

	update_device.set_defaults(func = command_devices_update)



	delete_device = device_parsers.add_parser(
		'delete',
		help = 'Delete an existing PushBullet device.',
	)

	delete_device.add_argument(
		'iden',
		type = str,
		help = 'The ID of the device',
	)

	delete_device.set_defaults(func = command_devices_delete)

def add_contact_commands(parsers):
	contact_parsers = parsers.add_subparsers()

	contact_parsers.add_parser(
		'list',
		help = 'List all contacts.',
	).set_defaults(func = command_contacts_list)



	create_contact = contact_parsers.add_parser(
		'create',
		help = 'Create a new contact.',
	)

	create_contact.add_argument(
		'name',
		type = str,
		help = 'The name of the contact',
	)

	create_contact.add_argument(
		'email',
		type = str,
		help = 'The contact\'s email',
	)

	create_contact.set_defaults(func = command_contacts_create)



	update_contact = contact_parsers.add_parser(
		'update',
		help = 'Update an existing contact.',
	)

	update_contact.add_argument(
		'iden',
		type = str,
		help = 'The ID of the contact',
	)

	update_contact.add_argument(
		'--name',
		type    = str,
		default = None,
		help    = 'Set the name of the contact',
	)

	update_contact.add_argument(
		'--email',
		type    = str,
		default = None,
		help    = 'Set the email of the contact',
	)

	update_contact.set_defaults(func = command_contacts_update)



	delete_contact = contact_parsers.add_parser(
		'delete',
		help = 'Delete an existing contact.',
	)

	delete_contact.add_argument(
		'iden',
		type = str,
		help = 'The ID of the contact',
	)

	delete_contact.set_defaults(func = command_contacts_delete)

def add_push_commands(parsers):
	push_parsers = parsers.add_subparsers()

	send_push = push_parsers.add_parser(
		'send',
		help = 'Send a push notification.',
	)

	target_group = send_push.add_mutually_exclusive_group(required = True)

	target_group.add_argument(
		'--device_iden',
		type = str,
		help = 'A device ID',
	)

	target_group.add_argument(
		'--email',
		type = str,
		help = 'An email address',
	)

	target_group.add_argument(
		'--channel_tag',
		type = str,
		help = 'A channel tag',
	)

	target_group.add_argument(
		'--client_iden',
		type = str,
		help = 'An OAuth client ID',
	)

	send_push.add_argument(
		'push_type',
		type    = str,
		choices = pb4py.Client.PUSH_TYPES,
		help    = 'The type of push to send',
	)

	send_push.add_argument(
		'--title',
		type    = str,
		default = None,
		help    = 'The title of the push (only used for note and link type pushes)',
	)

	send_push.add_argument(
		'--body',
		type    = str,
		default = None,
		help    = 'The body of the push',
	)

	send_push.add_argument(
		'--url',
		type    = str,
		default = None,
		help    = 'The URL of the push (only used for link pushes)',
	)

	send_push.add_argument(
		'--file-path',
		dest = 'file_path',
		type = str,
		help = 'The path to the file (only used for file pushes)',
	)

	send_push.add_argument(
		'--file-name',
		dest    = 'file_name',
		type    = str,
		default = None,
		help    = 'The name of the file (only used for file pushes), by dfeault this is the name of the file',
	)

	send_push.add_argument(
		'--file-type',
		dest    = 'file_type',
		type    = str,
		default = None,
		help    = 'The MIME type of the file (only used for file pushes), by default the MIME type is guessed',
	)

	send_push.set_defaults(func = command_push_send)



	push_history = push_parsers.add_parser(
		'history',
		help = 'Get your push history.',
	)

	push_history.add_argument(
		'--filter-type',
		type    = str,
		choices = pb4py.Client.PUSH_TYPES,
		help    = 'Filter the pushes by their type',
	)

	push_history.set_defaults(func = command_push_history)



	dismiss_push = push_parsers.add_parser(
		'dismiss',
		help = 'Dismiss a push.',
	)

	dismiss_push.add_argument(
		'iden',
		type = str,
		help = 'The push ID',
	)

	dismiss_push.set_defaults(func = command_push_dismiss)



	delete_push = push_parsers.add_parser(
		'delete',
		help = 'Delete a push',
	)

	delete_push.add_argument(
		'iden',
		type = str,
		help = 'The push ID',
	)

	delete_push.set_defaults(func = command_push_delete)

def add_subscription_commands(parsers):
	subscription_parsers = parsers.add_subparsers()

	subscription_parsers.add_parser(
		'list',
		help = 'List your subscriptions',
	).set_defaults(func = command_subscriptions_list)



	unsubscribe_to_channel = subscription_parsers.add_parser(
		'subscribe',
		help = 'Subscribe to a channel',
	)

	unsubscribe_to_channel.add_argument(
		'tag',
		help = 'The channel tag',
	)

	unsubscribe_to_channel.set_defaults(func = command_subscriptions_unsubscribe)

def add_channel_commands(parsers):
	channel_parsers = parsers.add_subparsers()

	channel_info = channel_parsers.add_parser(
		'info',
		help = 'Get information about a subscription.',
	)

	channel_info.add_argument(
		'tag',
		type = str,
		help = 'The channel tag',
	)

	channel_info.set_defaults(func = command_channel_info)



	subscribe = channel_parsers.add_parser(
		'subscribe',
		help = 'Subscribe to a channel.',
	)

	subscribe.add_argument(
		'tag',
		help = 'The channel tag',
	)

	subscribe.set_defaults(func = command_channel_subscribe)

def add_parser_commands(parsers):
	parsers.add_parser(
		'generate-config',
		help = 'Generate a sane set of config options. These can then bet put in the ~/.pb4pyrc file.',
	).set_defaults(func = command_generate_default_config)

	add_device_commands(parsers.add_parser(
		'devices',
		help = 'Manage connected devices.',
	))

	add_contact_commands(parsers.add_parser(
		'contacts',
		help = 'Manage contacts.',
	))

	parsers.add_parser(
		'me',
		help = 'Get information about yourself.',
	).set_defaults(func = command_me_get)

	add_push_commands(parsers.add_parser(
		'pushes',
		help = 'Manage pushes',
	))

	add_subscription_commands(parsers.add_parser(
		'subscriptions',
		help = 'Manage subscriptions',
	))

	add_channel_commands(parsers.add_parser(
		'channels',
		help = 'Manage channels',
	))

def parse_args():
	parser = argparse.ArgumentParser(
		description = 'A CLI command for working with PushBullet',
	)

	command_parsers = parser.add_subparsers(title = 'commands')
	add_parser_commands(command_parsers)

	return parser.parse_args()



def prompt(question, default = "yes"):
	"""
	Ask a yes/no question via raw_input() and return their answer.

	"question" is a string that is presented to the user.
	"default" is the presumed answer if the user just hits <Enter>.
		It must be "yes" (the default), "no" or None (meaning
		an answer is required of the user).

	The "answer" return value is True for "yes" or False for "no".
	"""

	valid = {'yes': True, 'y': True, 'ye': True, 'no': False, 'n': False}
	if default is None:
		options = ' [y/n] '
	elif default == 'yes':
		options = ' [Y/n] '
	elif default == 'no':
		options = ' [y/N] '
	else:
		raise ValueError('invalid default answer: \'%s\'' % default)

	while True:
		sys.stdout.write(question + options)
		choice = raw_input().lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			sys.stdout.write('Please respond with \'yes\' or \'no\' (or \'y\' or \'n\').\n')

def build_table(data, columns):
	return tabulate.tabulate(
		[
			[
				row[column] if column in row else ''
				for column in columns
			]
			for row in data
		],
		[col.replace('_', ' ').capitalize() for col in columns]
	)



def client_command(func):
	def wrapper(*args, **kwargs):
		client = pb4py.Client()

		return func(client, *args, **kwargs)

	return wrapper

def command_generate_default_config(args):
	config = {
		'auth': {
			'type':       'basic',
			'access_token': 'deadbeef',
		},
	}

	print(json.dumps(config, indent = 4, sort_keys = False))

@client_command
def command_devices_list(client, args):
	devices = client.devices()

	print(build_table(devices, ['iden', 'nickname', 'type']))

@client_command
def command_devices_create(client, args):
	client.create_device(args.name, args.device_type)

	print('Device created')

@client_command
def command_devices_update(client, args):
	updates = {
		k: getattr(args, k)
		for k in ['nickname', 'type']
		if getattr(args, k) is not None
	}

	client.update_device(args.iden, **updates)

	print('Device updated')

@client_command
def command_devices_delete(client, args):
	device = args.iden
	confirm = prompt('Are you sure you want to delete device {}?'.format(device), default = 'no')
	if not confirm:
		return

	client.delete_device(device)

	print('Device deleted')

@client_command
def command_contacts_list(client, args):
	contacts = client.contacts()

	print(build_table(contacts, ['iden', 'name', 'email']))

@client_command
def command_contacts_create(client, args):
	client.create_contact(args.name, args.email)

	print('Contact created')

@client_command
def command_contacts_update(client, args):
	updates = {
		k: getattr(args, k)
		for k in ['name', 'email']
		if getattr(args, k) is not None
	}

	client.update_contact(args.iden, **updates)

	print('Contact updated')

@client_command
def command_contacts_delete(client, args):
	contact = args.iden

	confirm = prompt('Are you sure you want to delete contact {}?'.format(contact), default = 'no')
	if not confirm:
		return

	client.delete_contact(contact)

	print('Contact deleted')

@client_command
def command_me_get(client, args):
	me = client.me()

	print(build_table([me], ['name', 'email']))

@client_command
def command_push_send(client, args):
	push_type = args.push_type
	if push_type == 'file':
		if not args.file_path:
			raise ValueError('No file was specified')

		args.file_url = client.upload_file(
			args.file_path,
			filename  = args.file_name,
			file_type = args.file_type,
		)['file_url']

		push_data = {
			k: getattr(args, k)
			for k in ['title', 'body', 'file_name', 'file_type', 'file_url']
			if getattr(args, k) is not None
		}
	elif push_type == 'link':
		if not args.url:
			raise ValueError('No URL was given')

		push_data = {
			k: getattr(args, k)
			for k in ['title', 'body', 'url']
			if getattr(args, k) is not None
		}
	elif push_type == 'note':
		push_data = {
			k: getattr(args, k)
			for k in ['title', 'body']
			if getattr(args, k) is not None
		}

	push_data.update({
		k: getattr(args, k)
		for k in ['device_iden', 'email', 'channel_tag', 'client_iden']
		if getattr(args, k) is not None
	})

	client.push(push_type, **push_data)

	print('Sent push')

@client_command
def command_push_history(client, args):
	pushes = client.push_history()

	if len(pushes) == 0:
		print('No pushes :\'(')
		return

	if args.filter_type:
		pushes = [push for push in pushes if push['type'] == args.filter_type]

	pushes = {
		push_type: [push for push in pushes if push['type'] == push_type]
		for push_type in pb4py.Client.PUSH_TYPES
	}

	for push_type in pb4py.Client.PUSH_TYPES:
		print()

		pushes_of_type = pushes[push_type]
		if len(pushes_of_type) == 0:
			continue

		if push_type == 'file':
			columns = ['iden', 'sender_name', 'sender_email', 'file_url']
		elif push_type == 'link':
			columns = ['iden', 'sender_name', 'sender_email', 'title', 'body', 'url']
		elif push_type == 'note':
			columns = ['iden', 'sender_name', 'sender_email', 'title', 'body']

		print('===== ' + push_type.capitalize() + ' =====')
		print(build_table(pushes_of_type, columns))

@client_command
def command_push_dismiss(client, args):
	push = args.iden

	confirm = prompt('Are you sure you want to dismiss push {}?'.format(push), default = 'no')
	if not confirm:
		return

	client.dismiss_push(push)

	print('Push dismissed')

@client_command
def command_push_delete(client, args):
	push = args.iden

	confirm = prompt('Are you sure you want to delete push {}?'.format(push), default = 'no')
	if not confirm:
		return

	client.delete_push(push)

	print('Push deleted')

@client_command
def command_subscriptions_list(client, args):
	subscriptions = client.subscriptions()

	for subscription in subscriptions:
		channel = subscription['channel']

		subscription['name']        = channel.get('name',        '')
		subscription['tag']         = channel.get('tag',         '')
		subscription['website_url'] = channel.get('website_url', '')
		subscription['description'] = channel.get('description', '')

	print(build_table(subscriptions, ['iden', 'name', 'tag', 'website_url', 'description']))

@client_command
def command_subscriptions_unsubscribe(client, args):
	channel = args.tag

	confirm = prompt('Are you sure you want to unsubscribe from this channel?', default = 'no')
	if not confirm:
		return

	client.unsubscribe_to_channel(channel)

	print('Unsubscribed')

@client_command
def command_channel_info(client, args):
	channel = client.get_channel_info(args.tag)

	print(build_table([channel], ['iden', 'name', 'tag', 'subscriber_count', 'website_url', 'description']))

@client_command
def command_channel_subscribe(client, args):
	channel = args.tag

	client.subscribe_to_channel(channel)

	print('Subscribed')



def main():
	args = parse_args()

	try:
		args.func(args)
	except pb4py.exceptions.PB4PyException as ex:
		print(ex)

if __name__ == '__main__':
	main()


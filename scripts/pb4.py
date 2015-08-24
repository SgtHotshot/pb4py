#!/usr/bin/env python

from __future__ import print_function

import argparse
import json
import tabulate

import pb4py



def add_device_commands(parsers):
	device_parsers = parsers.add_subparsers()

	device_parsers.add_parser(
		'list',
		help = 'List all devices.',
	).set_defaults(func = command_devices_list)

def add_parser_commands(parsers):
	parsers.add_parser(
		'generate-config',
		help = 'Generate a sane set of config options. These can then bet put in the ~/.pb4pyrc file.',
	).set_defaults(func = command_generate_default_config)

	add_device_commands(parsers.add_parser(
		'devices',
		help = 'Manage connected devices.',
	))

def parse_args():
	parser = argparse.ArgumentParser(
		description = 'A CLI command for working with PushBullet',
	)

	command_parsers = parser.add_subparsers(title = 'commands')
	add_parser_commands(command_parsers)

	return parser.parse_args()



def build_table(data, columns):
	return tabulate.tabulate(
		[
			[row[column] for column in columns]
			for row in data
		],
		[col.capitalize() for col in columns]
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

	print(build_table(devices, ['nickname', 'type']))



def main():
	args = parse_args()

	try:
		args.func(args)
	except Exception as ex:
		print(ex)

if __name__ == '__main__':
	main()


from setuptools import setup, find_packages

import os.path

with open('README.md', 'r') as readme:
	long_description = readme.read()

setup(
	name             = 'pb4py',
	version          = '1.0.0.0',
	description      = 'Python API for PushBullet',
	long_description = long_description,
	author           = ['sgthotshot', 'cadyyan'],
	url              = 'https://www.sgthotshot.com/pb4py',
	download_url     = 'https://github.com/SgtHotshot/pb4py/tarball/1.1',
	packages         = find_packages(),
	scripts          = [os.path.join('scripts', 'pb4.py')],
	keywords         = ['PushBullet', 'notifications', 'messaging'],
	classifiers      = [],
	install_requires = [
		'requests',
		'tabulate',
	],
)


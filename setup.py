from setuptools import setup, find_packages

setup(
	name             = 'pb4py',
	version          = '1.0.0.0',
	description      = 'Python API for PushBullet',
	author           = ['sgthotshot', 'cadyyan'],
	url              = 'https://www.sgthotshot.com/pb4py',
	packages         = find_packages(),
	install_requires = [
		'requests',
	],
)


from setuptools import setup, find_packages

setup(
	name             = 'pb4py',
	version          = '1.0.0.0',
	description      = 'Python API for PushBullet',
	author           = ['sgthotshot', 'cadyyan'],
	url              = 'https://www.sgthotshot.com/pb4py',
	download_url	 = 'https://github.com/SgtHotshot/pb4py/tarball/1.1',
	packages         = find_packages(),
	keywords		 = ['PushBullet', 'notifications', 'messaging'],
	classifiers		 = [],
	install_requires = [
		'requests',
	],
)


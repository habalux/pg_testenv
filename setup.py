from setuptools import setup

setup(
	name='pg_testenv',
	version="0.1",
	author="Teemu Haapoja",
	author_email="teemu.haapoja@gmail.com",
	description="PostgreSQL test instance creator",
	license="BSD",
	scripts = [
		'pg_testenv'
	],
)

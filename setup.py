from setuptools import setup

setup(
	name='pg_testenv',
	version="0.2",
	author="Teemu Haapoja",
	author_email="teemu.haapoja@gmail.com",
	description="PostgreSQL test instance creator",
	license="BSD",
	install_requires=['psycopg2'],
	packages=['pgtestenv'],
	scripts = [
		'pg_testenv'
	],
)

Using the python module
=======================

To use the python module, you need to import :py:class:`pgtestenv.instance.PgInstance` to your code

.. code-block:: python

	# Import the PgInstance class
	from pgtestenv.instance import PgInstance

	# Create a new instance on the relative directory 'testdb'
	pg = PgInstance("testdb")

	# Initialize database with PostgreSQL version 9.1
	# and set the default port to 5435
	pg.initdb('9.1',5435)

	# Start the instance
	pg.start()

See below for a more accurate description.

PgInstance interface
--------------------

.. method:: PgInstance.__init__(self, path, clean_on_delete=False)

	Initialize the object 

.. method:: PgInstance.info(self)

	Return a string description of the instance

.. method:: PgInstance.initdb(self, version, port, encoding="UTF-8", locale="en_US.UTF-8", superuser="postgres")

	Initialize the database on disk.

.. method:: PgInstance.start(self, port=None)

	Start up the database, optionally on a different port

.. method:: PgInstance.stop(self)

	Stop the database

.. method:: PgInstance.test_connection(self, *args, **kwargs)

	Test that the database can be reached
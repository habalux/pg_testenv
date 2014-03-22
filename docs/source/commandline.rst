Using the command line helper
=============================

Initializing a data directory
-----------------------------

.. code-block:: bash

	pg_testenv testdb initdb 9.1

If everything goes well, you should see a new directory *testdb*


Starting up the instance
------------------------

You can start the server with the following command:

.. code-block:: bash

	pg_testenv testdb start


This command starts the server with the port number defined with initdb. You can also specify a different port number:

.. code-block:: bash

	pg_testenv testdb start --port=5445

Stopping the instance
---------------------

.. code-block:: bash

	pg_testenv testdb stop

This uses *-m fast* to stop the server, so it will kick out any existing connections and then shut down the instance.

Managing the PostgreSQL config files
------------------------------------

This will be supported in a future version in some way, until then you can manually edit any required settings.

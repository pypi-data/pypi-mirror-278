
.. highlight:: ini

Integrating the POS
===================

The general process of integrating a POS is roughly the same (so far)
regardless of which POS system is involved.  Here we describe the
setup etc.

We will use CORE-POS as our example, for a few reasons, not least of
which is that it's also free (libre) software.  See
:ref:`pos-integration` for links to others.


Install Packages
----------------

Please remember to activate your virtual environment.

The first thing is, you must install the POS integration packages.
The packages for CORE-POS are publiclly available, in which case if
you just want the latest releases:

.. code-block:: sh

   pip install tailbone-theo[app,corepos]

Or if you want to run from source then you can clone/install these:

* https://kallithea.rattailproject.org/rattail-project/pycorepos
* https://kallithea.rattailproject.org/rattail-project/rattail-corepos
* https://kallithea.rattailproject.org/rattail-project/tailbone-corepos

But then just in case, do also run the above command as well, to
ensure all dependencies are got.


Modify Config
-------------

You must tell Alembic how to find all schema extensions for your POS
integration package.  Modify ``/srv/envs/theo/app/rattail.conf`` per
the following.

The default contains::

   [alembic]
   version_locations = rattail.db:alembic/versions

But you now instead need something like::

   [alembic]
   version_locations = rattail_corepos.db:alembic/versions rattail.db:alembic/versions

Note that the POS integration path should come before the default path
there.

In the same config file, you should declare your integration to Theo::

   [theo]
   integrate_corepos = true


Migrate Database
----------------

Most integrations will require some extra tables installed to your
database.  But installing them is no different than any other
migration, i.e. just run the normal commands:

.. code-block:: sh

   cd /srv/envs/theo
   bin/alembic -c app/rattail.conf upgrade heads


Import POS Data
---------------

This process can vary a little but a couple of concepts will be useful
regardless.

First is that data "versioning" must be considered here.  Theo
normally will use the versioning feature, i.e. whenever a record
changes, a new "version" record is also created for it.  The logic
behind this has some performance cost, which is by far most pronounced
when there are a "lot" of changes within the same database session.

Therefore a workaround is employed when the database is initially
populated: the versioning feature is disabled for the main import, and
then version records are created for the initial data in a separate
step.  So the first import command always includes ``--no-versiong``:

.. code-block:: sh

   cd /srv/envs/theo
   bin/rattail -c app/quiet.conf -P import-corepos-api --no-versioning

Once all the data lives in Theo, then capture the initial version
records for everything.

.. code-block:: sh

   bin/rattail -c app/quiet.conf -P --runas corepos import-versions -m "initial data from POS"

Note the ``--runas`` arg above, which declares the Theo username
responsible.  The user must already exist within Theo, but can be
created via the Theo web app.


Ongoing Sync
------------

There are a few ways to do the ongoing "sync" between the POS system
and Theo.  For now we will only describe a very basic sync which
happens once per night, although could also be used hourly etc.

The idea here is basically just like the initial data import, although
should not need the versioning workaround.  So one command, something
like:

.. code-block:: sh

   cd /srv/envs/theo
   bin/rattail -c app/quiet.conf --runas corepos import-corepos-api

This is a very basic example, in particular does not handle
"deletions" which may occur in CORE.  For now though we'll leave it at
that, hopefully more to come later.


.. highlight:: sh

Installing Manually
===================

See also :doc:`/quickstart`, as it automates many of the steps below.

More general details and background may be found in the Rattail
Manual; see :doc:`rattail-manual:base/index` for that.  Here of course
we will focus on Theo, so will be less generic.

The initial setup below will *not* include any POS integration, but
that may optionally be added, and is described in another section.


Prerequisites
-------------

* Python 3.6+
* PostgreSQL

Note that PostgreSQL need not run on the same machine as the Theo app,
it just needs to be accessible over the network by Theo.

These docs assume Linux for the Theo machine, but it is believed that
with minimal tweaks this should work on Windows as well.  However it
should be noted that Windows does pose some issues, and this all
likely will work "better" on Linux at this point.  Windows support
should be considered experimental.

(In any case PostgreSQL can run on a Windows machine if you prefer
that.)


Virtual Environment
-------------------

These docs will assume ``/srv/envs`` for the "home folder" of your
virtual environments.

Create a virtual environment for Theo::

   mkdir -p /srv/envs
   python3 -m venv /srv/envs/theo

Now activate it with::

   source /srv/envs/theo/bin/activate

Remember you can deactivate the virtual environment with::

   deactivate

But your environment should be *active* for all commands below.


Install Packages
----------------

In a production environment you probably would want to install
"official" released packages for Theo etc.  That can be done for
instance like::

   pip install tailbone-theo[app]

That is just an example and would not install any POS integration
packages, only Theo proper.

However in practice you may want to clone the source packages and
install those in "editable" mode instead.  In a true development
environment we would suggest keeping the source code *outside* of the
virtual environment, so that is what we'll describe here.

First make and/or move to the parent folder for your source code,
e.g.::

   mkdir -p ~/src
   cd ~/src

Then clone any packages you don't yet have, e.g.::

   git clone https://kallithea.rattailproject.org/rattail-project/rattail
   git clone https://kallithea.rattailproject.org/rattail-project/tailbone
   git clone https://kallithea.rattailproject.org/rattail-project/theo

Finally install all packages to your virtual environment, e.g.::

   pip install -e ~/src/rattail
   pip install -e ~/src/tailbone
   pip install -e ~/src/theo

But just to be sure no dependencies are missed, you still should run
the same command as would be used in production, e.g.::

   pip install tailbone-theo[app]

Note that this command should always be ran *last* after you have
installed all your source packages.


Make Config Files
-----------------

The ``dev/bootstrap.py`` script referenced by :doc:`/quickstart` will
install four different config files, but we'll only install three
here.

First create the "app" folder (will be at ``/srv/envs/theo/app``)::

   cd /srv/envs/theo
   bin/rattail make-appdir

One of the config files is quite simple and can be copied "as-is" from
elsewhere, but two of them will require some modification depending on
your setup etc.  Starting point examples are available for the latter
two, but cannot be used "as-is" due to their nature.

Note that all config files will go directly in the "app" folder we
just made above.

We'll do the more complicated ones first.  You can grab copies of them
from Theo source code:

* `rattail.conf <https://kallithea.rattailproject.org/rattail-project/theo/rawfile/master/dev/rattail.conf>`_
* `web.conf <https://kallithea.rattailproject.org/rattail-project/theo/rawfile/master/dev/web.conf>`_

Put each copy in your Theo "app" folder and edit as needed, in
particular replacing ``<ENVDIR>`` and similar strings (e.g. ``<SEP>``
should be either ``/`` on Linux or ``\`` on Windows).

And now for the easy one, you can do this::

   cd /srv/envs/theo
   bin/rattail -c app/rattail.conf make-config -T quiet -O app


Initialize Database
-------------------

On your PostgreSQL server, if you haven't already, create the user
with which Theo should connect.  We suggest "rattail" for the
username::

   sudo -u postgres createuser -P rattail

Also create the database for Theo::

   sudo -u postgres createdb -O rattail theo

Now back on the Theo server (if different), install the schema to the
database (NB. this assumes your ``rattail.conf`` file correctly points
to the PostgreSQL DB)::

   cd /srv/envs/theo
   bin/alembic -c app/rattail.conf upgrade heads

You also should create your admin user in Theo, named whatever you
like::

   bin/rattail -c app/quiet.conf make-user myusername --admin --full-name "My Actual Name"


Run Web App
-----------

With all the above in place you can run the web app::

   cd /srv/envs/theo
   bin/pserve --reload file+ini:app/web.conf

And then browse the app at http://localhost:9080/

Note that this is a basic setup and does not cause the web app to run
in the background or after reboot etc.  This type of setup is most
useful for development.

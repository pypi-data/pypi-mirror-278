
.. highlight:: sh

Quick Start
===========

This should get you up and running in minutes, with a "bare" Theo setup,
meaning no POS integration.  (You can add that later if desired.)

Clone the source code for Theo wherever you like, e.g. ``~/src/theo``::

   mkdir -p ~/src
   cd ~/src
   git clone https://kallithea.rattailproject.org/rattail-project/theo

Your local PostgreSQL service should be available, and user (named ``rattail``)
and DB (named ``theo``) created::

   sudo apt install postgresql
   sudo -u postgres createuser -P rattail
   sudo -u postgres createdb -O rattail theo

Make and activate a virtual environment, e.g. ``/srv/envs/theo``::

   mkdir -p /srv/envs
   python3 -m venv /srv/envs/theo
   source /srv/envs/theo/bin/activate

With the virtual environment active, run the development bootstrap script::

   python3 ~/src/theo/dev/bootstrap.py

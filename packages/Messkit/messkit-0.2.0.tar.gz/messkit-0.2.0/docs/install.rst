
.. highlight:: sh

Installation
============

We'll try to keep this brief but link to further reading where needed.


Prerequisites
-------------

* Linux strongly recommended
* Python 3
* database in PostgreSQL or MySQL (or ??)

Linux is recommended because effectively "all" production testing has
happened on Debian and Ubuntu specifically.  But the project is all
Python so should run anywhere as long as the code is accounting for
that...which to be honest it may not be in all places yet.

The assumption is that you already have Python 3, unless on Windows in
which case see :doc:`rattail-manual:base/install/windows/python`.

You can ostensibly use any backend `supported by SQLAlchemy`_ to store
your Messkit database; however in practice PostgreSQL has had a
gazillion times more production testing and is highly recommended.
MySQL/MariaDB also have seen some basic testing and are believed to
work fine.

.. _`supported by SQLAlchemy`: https://docs.sqlalchemy.org/en/13/dialects/index.html

Note that the database need not live on the same machine as the
Messkit app.

The Messkit installer currently only supportes PostgreSQL and
MySQL/MariaDB, so if another backend is desired it just means the
installer can't automate setup for you, but manual setup is still
possible.


Messkit
-------

Create a virtual environment for Messkit, e.g.::

   python3 -m venv /path/to/envs/messkit

If you're new to these see also :doc:`rattail-manual:base/venv`.

Be sure to activate your virtual environment::

   source /path/to/envs/messkit/bin/activate

Next install the Messkit package to your environment::

   pip install Messkit

Now setup your database backend.  Messkit will need a database, and it
will need to connect to that database with a particular set of user
credentials.

Depending on your backend type, create the user account.  The default
username is ``rattail`` so we'll assume that here.  Whatever username
and password you set will be needed for the final Messkit setup.

PostgreSQL::

   sudo -u postgres createuser -P rattail

MySQL::

   sudo mysql -e "create user rattail@localhost"
   sudo mysql -e "alter user rattail@localhost identified by 'THEPASSWORD'"

Next create the database itself.

PostgreSQL::

   sudo -u postgres createdb -O rattail messkit

MySQL::

   sudo mysqladmin create messkit
   sudo mysql -e "grant all on messkit.* to rattail@localhost"

Finally run the Messkit installer.  When it asks for **db type** you
can enter ``mysql`` or just accept the ``postgresql`` default.  You
are advised to answer "yes" to all yes/no questions::

   messkit -n install

With that complete you should be able to run the web app with::

   cd /path/to/envs/messkit
   bin/pserve file+ini:app/web.conf

Please note, you should have created an admin user during the Messkit
installer.  You should be able to login to the web app with those
credentials, but by default even an "admin" user can't do much of
anything.

However an admin user has a special power - they can "become root"
which means the same as it does for Linux.  When you do this all
features which exist become unlocked.  The expectation for a
"production" app is that you would define roles and grant them
permissions etc. as needed.  But while testing you can just "become
root" and not really worry about the permissions.


Upgrading
---------

Upgrades are done directly in the web app, and basic details of each
are recorded.

Default menu location is Admin -> Messkit Upgrades.  Create a new
upgrade, make sure it is enabled, then execute it.  That's all!

Although, the default upgrade script will not actually restart the web
app for you, so after an upgrade completes successfully you should
restart the web app manually.


Starting Over
-------------

A major goal for Messkit is to make "starting over" a simple thing, to
encourage users to experiment with it.  Maybe you even keep one app in
production while having others reserved for trying new things.

The installer is of course a big part of that, so hopefully it's easy
enough, but suggestions for improvements are always welcome!

But depending on your situation you may prefer to "destroy" the
previous attempt before installing a new app etc.  Really that is just
2 steps:

Remove entirely your "app" folder, e.g.::

   cd /path/to/envs/messkit
   rm -rf app

Then drop and re-create your database.  Commands for creating a
database are shown above, but here are the drops.

PostgreSQL::

   sudo -u postgres dropdb messkit

MySQL::

   sudo mysqladmin drop messkit

With that done you can re-run the installer::

   messkit -n install

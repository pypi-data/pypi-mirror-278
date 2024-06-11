
Features
========

This page lists the "completed" features for Messkit.  All of the
following are considered working and stable.

Also note, here we only highlight features deemed Messkit-specific.
Since Messkit is built on top of lots of other tech, there are `many
more features`_ which have been complete for years.  Most of those
underlying features assumed a programmer would "glue" components
together in code, whereas Messkit is trying to let the admin user do
that via web app instead.  So this feature list reflects only the
Messkit-specific goals.

.. _`many more features`: https://rattailproject.org/moin/TheBigTour


Configurable Menus
------------------

Nearly the entire top-level menu is editable.  The "user" menu (far
right of top menu) is *not* editable, but all other top-level menus
are "fully" editable.

(More complexity should be allowed yet, e.g. adding a submenu, but the
common needs are met already.)

Go to the App Settings page (/settings/app/) and from the "Go To
Configure" dropdown choose Menus.


Configurable Views
------------------

This is related to the previous point (e.g. a menu entry usually
references some sort of view), but is definitely a separate concern.

First to clarify..  A "view" in this context really means a "Python
module containing view logic" and that "view logic" is what responds
to user requests and displays data etc.  Most often a particular view
is tied to a particular table in the DB.

Messkit comes with many views built-in, but not all will be relevant
to you.  For instance you might need to see Employees but not
Products.

Messkit allows for any such built-in view to be:

* disabled
* enabled, using default view module
* enabled, using custom view module

Go to the App Settings page (/settings/app/) and from the "Go To
Configure" dropdown choose Included Views.


Custom Reports
--------------

Messkit comes with "some" reports built-in.  However there are very
few and they serve mostly as examples.

First to clarify, a "report" in this context really means a "Python
module containing report logic" and that "report logic" is what
generates the output file.

Messkit allows you to create new reports (Python modules) to suit your
needs.  Reporting needs can vary wildly, so Messkit does not try to
provide the full interface to create a "complete" detailed report.
But it can generate some skeleton code and get you started in the
right direction.

More "flavors" of sample code generation should be added, but there
are some basic ones in place already.  Namely they allow for either
using raw SQL to query tables, or alternately can use the SQLAlchemy
models which then auto-generate the SQL needed.

At this time Messkit does not have any smarts about "other systems"
and therefore sample code it generates will only show how to query the
Messkit database.  As time goes on more sample code will be added,
which shows how to query other (e.g. POS) databases, as well as e.g.
web API for some systems.

Messkit "blends" the custom reports with its built-in reports, in the
user interface.  Meaning, if a user goes to generate a new report
(i.e. run a module to produce output) then they will see all available
reports in the same list.

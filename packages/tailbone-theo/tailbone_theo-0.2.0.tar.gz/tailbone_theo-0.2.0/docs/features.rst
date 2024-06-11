
Feature Overview
================

Theo tries to offer tools to complete "the order system" for an
organization.  We say "complete" because there is no reason to
necessarily "replace" existing systems, but can often just
"supplement" them instead.

The primary concerns for Theo at this point are:

* display and/or maintenance of general (customer/product) data
* create and manage "customer orders"
* assist with "purchasing workflows"
* data reporting and visualization

These are given a bit more explanation below.


General Data
------------

The most basic thing Theo can do, is to give the user a view of all
"general" (aka. "operational") data, i.e. customers, products, vendors
and the like.

The preferred scenario is where Theo integrates with your POS, in
which case this data would be imported from the POS and therefore be
"read-only" within Theo.

But if there is no POS integration in place then Theo can allow basic
CRUD operations on these tables as well.

Note that in *either case*, Theo will track "versions" for this data.
Every time a Theo record is changed, a copy of it is saved into a
versioning table.  This lets you see how any record changes over time.
If the change is done directly by a user in Theo, then "who" did it is
also recorded; otherwise the "who" will refer only to the system from
which the change came, i.e. your POS.


Customer Orders
---------------

Theo's "#1 feature" out of the box, is to offer a way to record and
track customer orders.

Arguably the most important piece of this feature, is the "New
Customer Order" page.  Here the user can enter in the customer and
product details for a new order.  When they submit the order it
becomes available for processing in subsequent steps in the workflow.

The user is therefore also able to track and update progress of any
order over time.  Ultimately each order is "finalized" somehow, and
nothing more will happen to it.  They are of course kept intact for
reporting etc.


.. _pos-integration:

POS Integration
---------------

Theo itself is merely a wrapper around the Rattail and Tailbone
packages, optionally with some POS integration packages thrown in as
well.  So far the following are supported:

* `CORE-POS <https://redmine.rattailproject.org/projects/corepos-integration>`_
* `ECRS Catapult <https://redmine.rattailproject.org/projects/catapult-integration>`_
* `LOC SMS <https://redmine.rattailproject.org/projects/locsms-integration>`_

If you have one of those then you will surely want to integrate it
with Theo.  But what would that give you?

The main thing is that Theo should import all customer and product
data from your POS system.  In some cases this can involve a
"real-time" sync, in other cases maybe an hourly import, etc.  With
this in place you should feel free to generally "trust" the data you
see in Theo as being accurate (i.e. matches POS).

Another common need is for Theo to "monitor" the POS transactions, and
e.g.  flag a customer order item as "paid for" or "delivered" whenever
it is seen rang up and sold to the customer.

It also is possible to tie "customer orders" into the "purchasing
workflows" - see next section.

But as of this writing, that's where Theo's ambitions end.  Theo does
not (yet?) intend to expose any way to write data back to the POS
system, for instance, other than what is described in next section.
However it's worth noting that some of the POS integration packages
used by Theo, *are* able to write back to the POS system, for various
things.


Purchasing Workflows
--------------------

Every retailer (presumably) must order product from the vendor, and
receive it etc.  Theo tries to offer some tools around that.  In
particular:


Ordering
~~~~~~~~

Some orgs have automatic (or "suggested") ordering in place.  If that
is your situation then great!  Theo will have less to offer you, but
you might still keep reading.

Other orgs must manually "assemble" their purchase orders and submit
them to the vendor.  Often the specific process will vary depending on
the vendor etc.

Theo therefore provides features to help with this:

* tools to assemble a purchase order
* tools to "convert" a purchase order from one format/system to another
* tools to inform buyer of relevant "customer orders"

A new purchase order may be created from scratch, and items scanned
into it.  Or if the vendor catalog is not terribly large, buyer can
edit the order as a "worksheet" which shows everything available from
the vendor.  A mobile interface is also possible, for in-aisle
scanning of shelf tags etc.

Once you have a purchase order assembled, Theo can be used to convert
it to another format if needed.  For instance you might create the PO
using Living Naturally software, but then you want a way to import the
result to your POS system.

To tie "customer orders" into this, Theo offers a way for buyers to
see at a glance which customer orders might be relevant to them, i.e.
based on the vendor/department for which they're assembling a purchase
order.  Buyer can then claim responsibility and add the customer order
item(s) to their purchase order.


Receiving
~~~~~~~~~

As with Ordering (above), Receiving may be done in several ways.  At
least it isn't ever automated, or shouldn't be unless you just want
bad inventory counts!

Theo again provides features to help:

* tools to receive the purchase order, i.e. indicate what was (not) received
* tools to update actual cost from invoice
* tools to "convert" receiving data from one format/system to another
* tools to inform receiver of relevant "customer orders"

Theo allows user to create a new "receiving" batch using any of the
following supported workflows:

* from scratch (aka. just start scanning this pile...)
* from digital PO (aka. scan "against" what is expected)
* from digital invoice (same as previous, but with accurate cost)
* from digital PO, with digital invoice (same as previous)

Again a mobile interface is possible, when applicable.  Often
receiving is paper-based; that can still be done, in which case user
would record the "exceptions" to Theo.  (This requires either a PO or
invoice however, cannot be from scratch.)

We assume that "receiving" is concerned only with keeping inventory
counts accurate, and managing "credits" (more on that below).  However
in practice, if there is an invoice available at time of receiving, it
often is useful to bring "costing" into it as well.  (Otherwise
costing can be a separate 3rd stage to the purchasing workflow, after
receiving has been completed.)

So the "convert" feature in this case is sort of 2-fold.  On the one
hand you have the "received quantities" to deal with, but also
(potentially) the "actual costs" for each item.  In any event once the
pertinent data is "settled" then Theo can convert however you need.

Finally to tie "customer orders" into this, Theo gives the receiver a
way to see at a glance, which customer order items are relevant to
them, i.e. based on the vendor/department for which they're receiving
a purchase order.


Costing
~~~~~~~

This refers to the updating of actual cost information, e.g. as
obtained from the vendor invoice for a purchase order.

In practice so far, nobody has wanted this as a separate step; instead
it always gets lumped into Receiving (above).  Until that changes
we'll just leave it at that.


Credits
~~~~~~~

This gets its own section although it's closely related to Receiving
and/or Costing (above).

When the receiver indicates a given item was not received, or was
damaged/expired etc. then Theo is able to record that.  Each such
"credit" can then be tracked and updated by the user, as needed.

Note that there is little/no "magic" here, just a simple way to keep
tabs on vendor credits.


Reporting / Visualization
-------------------------

As of this writing Theo does not have any "useful" reports; however
the framework for them is in place.  Stay tuned, as this feature will
grow as more Theo systems are installed and real-world needs come up.

Additionally, some work has begun on a "dashboard" app using `Dash`_.

.. _Dash: https://dash.plotly.com/

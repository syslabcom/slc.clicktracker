Introduction
============

slc.clicktracker injects tracking javascript into marked pages. That
javascript then calls back so that we can track which users are viewing
what pages. The basic use case for this is to make sure people in your
organisation actually read a document before they vote against it in a
meeting.

Why javascript? It introduces no delays in the loading of pages, instead
deferring the collection of stats to an aysnchronous process that happens after
the page loads. It also ensures that stats are collected from real browsers and
it is in a sense more accurate, it only registers a payload after the page was
successfully rendered client side. It is of course easy to avoid being logged,
but the idea is to check for positive evidence, people who did read it.

Pluggable storage layer
=======================

The storage layer is designed to be pluggable. To implement a storage you need
to implement the IClickStorage interface. This basically requires the
implementation of two methods, logAccess (which puts data into the storage) and
getLog (which retrieves data from the storage). The storage layer is registered as
a utility using ZCML.

This product comes with an existing storage component that uses Postgresql. The
thinking behind this implementation is to avoid zodb bloat caused by frequent
writes.

Disabling tracking on content
=============================

To disable tracking for a view, mark the request with IContentIsIgnored early
on during the request, before any content is generated.

Configuration
=============

The postgresl configuration is stored in the plone registry. There is a
configlet in the plone control panel (Site Setup) where you can set the DSN
for connecting to the database server. The format of the DSN is as described in
the psycopg2 manual at http://initd.org/psycopg/docs/.

Database initialisation
=======================

After creating a new database for tracking purposes, you need to activate the
plpgsql language for this database. You should then load sql/db.sql into your
newly created database. This contains all the table definitions and the stored
procedure that does the actual work. For ease of use, there is also a
GenericSetup step to automate this. An example is provided below.

Example Postgresql Configuration
================================

Users of other databases often have some trouble understanding Postgresql's
authentication. Here is a simple step-by-step guide to configure
slc.clicktracker for a standard (as it ships for Debian based Linux
distributions) postgresql installation.

0. You need to install postgresql if you haven't done so yet. You will also
need the development headers. To do this on a Debian/Ubuntu machine type:

    sudo apt-get install postgresql libpq-dev

1. Become the postgresql user:

    sudo -u postgres -i

2. Log into the template1 database:

    psql template1

3. Create a user and a tracking database. The user needs to have the same name
as the system user running zope. Here is an example session for a user named
zope:

    template1=# create user zope;
    CREATE ROLE
    template1=# create database tracking owner zope;
    CREATE DATABASE
    template1=# \q

4. Install the plpgsql language into your database

    createlang plpgsql tracking

5. In your plone site, go to Site Setup, ClickTracker Setings, then configure
slc.clicktracker with the DSN:

    dbname=tracking

6. Now go to portal_setup, click the Import tab, then choose "slc.clicktracker
database setup" from the dropdown, and import all steps.

That's it. The mentioned default installation of Postgresql uses "ident"
authentication, which means there is no need to specify a user name and
password, all it needs is the name of the database.

NB: Please note that the above won't work if postgresql is installed on a host
other than localhost, if you run a distribution where postgresql is not set up
to do ident authentication be default, or if you're running Windows. In that
case, please consult the postgresql documentation for details on the
pg_hba.conf file, and the psycopg2 documentation for details on the dsn.

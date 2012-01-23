Introduction
============

slc.clicktracker injects tracking javascript into marked pages. That
javascript then calls back so that we can track which users are viewing
what pages. The basic use case for this is to make sure people in your
organisation actually read a document before they vote against it in a
meeting.

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

The postgresl configuration is stored in te plone registry. There is a
configlet in the plone control panel (Site Setup). The format of the DSN is as
described in the psycopg2 manual at http://initd.org/psycopg/docs/.

Database initialisation
=======================

After creating a new database for tracking purposes, you need to activate the
plpgsql language for this database. You should then load the db.sql into your
newly created database. This contains all the table definitions and the stored
procedure that does the actual work. An example is provided below.

Example Postgresql Configuration
================================

Users of other databases often have some trouble understanding Postgresql's
authentication. Here is a simple step-by-step guide to configure
slc.clicktracker for a standard (as it ships for Debian based Linux
distributions) postgresql installation.

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

5. As the zope user, load db.sql

    psql tracking < db.sql

6. Configure slc.clicktracker with the DSN:

    dbname=tracking

That's it. The mentioned default installation of Postgresql uses "ident"
authentication, which means there is no need to specify a user name and
password, all it needs is the name of the database.

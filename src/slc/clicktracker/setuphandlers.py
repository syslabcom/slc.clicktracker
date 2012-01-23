import os
import psycopg2
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from slc.clicktracker.interfaces import IClickTrackerSettings

PACKAGE_ROOT = os.path.dirname(os.path.realpath(__file__))

def setupDatabase(context):
    """ Do the initial database setup. """

    if context.readDataFile('slc.clicktracker-marker.txt') is None:
        return

    registry = queryUtility(IRegistry)
    dsn = registry.forInterface(IClickTrackerSettings).dsn
    f = open(os.path.join(PACKAGE_ROOT, 'sql', 'db.sql'), 'r')
    connection = psycopg2.connect(dsn)
    cursor = connection.cursor()
    cursor.execute(f.read())
    f.close()
    connection.commit()
    connection.close()

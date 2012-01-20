import psycopg2
from slc.clicktracker.interfaces import IClickStorage
from zope.interface import implements

class PostgresqlStorage(object):

    implements(IClickStorage)

    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            # TODO: Configure dsn from plone.registry
            self.connection = psycopg2.connect("dbname=izak")
        except psycopg2.OperationalError:
            self.connection = None

    @property
    def connected(self):
        if self.connection is None:
            return False
        return self.connection.closed == 0

    def logAccess(self, member, url):
        """ Log the given information, user visited url. """
        if not self.connected:
            self.connect()

        if self.connected:
            # TODO log to database
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT logclick(%(member)s, %(document)s) AS result",
                {'member': member, 'document': url})
            if cursor.fetchone()[0]:
                self.connection.commit()
                return True
        return False

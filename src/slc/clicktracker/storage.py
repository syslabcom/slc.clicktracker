import psycopg2
from zope.component import queryUtility
from zope.interface import implements
from plone.registry.interfaces import IRegistry
from slc.clicktracker.interfaces import IClickStorage, IClickTrackerSettings

class PostgresqlStorage(object):

    implements(IClickStorage)

    def __init__(self):
        self.connection = None

    def getSettings(self):
        registry = queryUtility(IRegistry)
        if registry is None:
            return None
        return registry.forInterface(IClickTrackerSettings)

    def connect(self):
        self.connection = None
        try:
            settings = self.getSettings()
            if settings is not None and settings.dsn is not None:
                self.connection = psycopg2.connect(settings.dsn)
        except psycopg2.OperationalError:
            pass

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

from thread import get_ident as get_thread_id
import psycopg2
from zope.component import queryUtility
from zope.interface import implements
from plone.registry.interfaces import IRegistry
from slc.clicktracker.interfaces import IClickStorage, IClickTrackerSettings

# mapping from thread-id to a connection, so we have one connection per thread
POOL = {}

class PostgresqlStorage(object):

    implements(IClickStorage)

    def getSettings(self):
        registry = queryUtility(IRegistry)
        if registry is None:
            return None
        return registry.forInterface(IClickTrackerSettings)

    @property
    def connection(self):
        tid = get_thread_id()
        c = POOL.get(tid, None)
        if c is not None and c.closed==0:
            return c

        settings = self.getSettings()
        if settings is not None and settings.dsn is not None:
            try:
                c = psycopg2.connect(settings.dsn)
            except psycopg2.OperationalError:
                return None

            POOL[tid] = c
            return c

    def logAccess(self, member, url):
        """ Log the given information, user visited url. """
        if self.connection is not None:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT logclick(%(member)s, %(document)s) AS result",
                {'member': member, 'document': url})
            if cursor.fetchone()[0]:
                self.connection.commit()
                return True
        return False

    def getLog(self, prefix):
        """ Obtain logged details for paths starting with prefix. """
        connection = self.connection
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT click.member,SUM(click.count) AS count, "
                "MAX(click.lastaccess) AS lastaccess FROM click INNER JOIN "
                "document ON (click.document=document.id) WHERE "
                "document.url LIKE %(prefix)s GROUP BY click.member",
                {'prefix': prefix + '%'})
            li = cursor.fetchall()
            connection.rollback() # Avoid idle connection in transaction
            return li
        return ()

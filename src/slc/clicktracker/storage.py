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
                c.autocommit = True # because we don't exactly need them
            except psycopg2.OperationalError:
                return None

            POOL[tid] = c
            return c

    def closeConnection(self):
        tid = get_thread_id()
        if POOL.has_key(tid):
            # This will also close the connection
            del(POOL[tid])

    def logAccess(self, member, path, url):
        """ Log the given information, user visited path via url. """
        if self.connection is not None:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT logclick(%(member)s, %(document)s, %(url)s) AS result",
                {'member': member, 'document': path, 'url': url})
            if cursor.fetchone()[0]:
                return True
        return False

    def getLog(self, prefix, order_by=None, order_reverse=False):
        """ Obtain logged details for paths starting with prefix. """
        connection = self.connection
        if connection is not None:
            order = {'member': 'click.member',
                     'url': 'click.url',
                     'count': 'count',
                     'lastaccess': 'lastaccess'}.get(order_by, 'click.member')


            cursor = connection.cursor()
            try:
                cursor.execute(
                    "SELECT click.member,SUM(click.count) AS count, "
                    "MAX(click.lastaccess) AS lastaccess, click.url FROM "
                    "click INNER JOIN document ON (click.document=document.id) "
                    "WHERE document.path LIKE %(prefix)s GROUP BY "
                    "click.member, click.url ORDER BY " + order + \
                    (order_reverse and " DESC" or ""),
                    {'prefix': prefix + '%'})
            except psycopg2.Error:
                self.closeConnection()
                return ()

            li = cursor.fetchall()
            return li
        return ()

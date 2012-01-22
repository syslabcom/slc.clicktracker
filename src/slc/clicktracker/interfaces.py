from zope.schema import TextLine
from zope.interface import Interface
from slc.clicktracker import MessageFactory as _

class IClickTrackerLayer(Interface):
    """Marker Interface used by as BrowserLayer
    """

class IClickStorage(Interface):
    """ Marker interface for storage utility. """

    def logAccess(user, path, url):
        """ Log the given information, user visited path with url. """

    def getLog(prefix, order_by=None, order_reverse=False):
        """ Find records for paths starting with prefix. """

class IClickTrackerSettings(Interface):
    """ So we can store some settings related to this product and the
        annotator.
    """
    dsn = TextLine(
        title=_(u'Database DSN'),
        description=_(u'Define the DSN for connecting to the database.'),
        required=True
    );

class IContentIsTracked(Interface):
    """ Marker interface for tracked content. """

class IContentIsIgnored(Interface):
    """ Glue this onto your request, eg. in a browser view, to disable
        tracking for that request. Avoid tracking certain views. """

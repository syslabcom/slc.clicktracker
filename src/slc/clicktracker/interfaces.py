from zope.interface import Interface

class IClickTrackerLayer(Interface):
    """Marker Interface used by as BrowserLayer
    """

class IClickStorage(Interface):
    """ Marker interface for storage utility. """

    def logAccess(user, url):
        """ Log the given information, user visited url. """

from zope.component import queryUtility
from Products.Five import BrowserView
from slc.clicktracker.interfaces import IClickStorage

class TrackerCallbackView(BrowserView):
    """ This is called via jquery POST. """
    def __call__(self):
        url = self.request.get('absolute_url', None)

        if(url is not None):
            storage = queryUtility(IClickStorage)
            member = self.context.restrictedTraverse(
                '@@plone_portal_state').member()

            storage.logAccess(str(member), url)
        return '' # No content

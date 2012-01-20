from Acquisition import aq_inner
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from slc.clicktracker.interfaces import IContentIsTracked

class JSTrackerViewlet(ViewletBase):
    """ Adds a bit of javascript to the top of the page with tracking code.
    """
    index = ViewPageTemplateFile('tracker.pt')

    def enabled(self):
        context = aq_inner(self.context)
        return IContentIsTracked.providedBy(context)

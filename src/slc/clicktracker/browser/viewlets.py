from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class JSTrackerViewlet(ViewletBase):
    """ Adds a bit of javascript to the top of the page with tracking code.
    """
    index = ViewPageTemplateFile('tracker.pt')

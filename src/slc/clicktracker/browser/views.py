from Acquisition import aq_inner
from zope.component import queryUtility
from zope.interface import alsoProvides, noLongerProvides
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.PloneBatch import Batch
from slc.clicktracker.interfaces import IClickStorage, IClickTrackerSettings
from slc.clicktracker.interfaces import IContentIsTracked, IContentIsIgnored
from slc.clicktracker.util import contentIsTracked
from slc.clicktracker import MessageFactory as _

class TrackerCallbackView(BrowserView):
    """ This is called via jquery POST. """
    def __call__(self):
        url = self.request.get('url', None)
        path = self.request.get('path', None)

        if(url is not None and path is not None):
            storage = queryUtility(IClickStorage)
            member = self.context.restrictedTraverse(
                '@@plone_portal_state').member()

            storage.logAccess(str(member), path, url)
        return '' # No content

class ClickTrackerSettingsForm(RegistryEditForm):
    schema = IClickTrackerSettings
    label = _(u'ClickTracker Settings')
    description = _(u"Use the settings below to configure "
        u"slc.clicktracker for this site")

class ClickTrackerControlPanel(ControlPanelFormWrapper):
    form = ClickTrackerSettingsForm

class TrackingSetupView(BrowserView):
    index = ViewPageTemplateFile("trackingsetup.pt")

    def tracked(self):
        """ Returns the context in our aq_chain that is tracked, or None. """
        context = aq_inner(self.context)
        return contentIsTracked(context)

    def isdirectlytracked(self):
        """ Returns True if our context is directly tracked. """
        context = aq_inner(self.context)
        return IContentIsTracked.providedBy(context)

    def log(self):
        b_start = self.request.get('b_start', 0)
        b_size = self.request.get('b_size', 20)
        sort_on = self.request.get('sort_on', 'member')
        sort_reverse = self.request.get('sort_reverse', '0') == '1'

        storage = queryUtility(IClickStorage)
        prefix = '/'.join(self.context.getPhysicalPath())
        log = [{'member': x[0], 'count': x[1],
                'lastaccess': x[2].strftime('%Y-%m-%d %H:%M:%S'),
                'url': x[3]} \
            for x in storage.getLog(prefix, order_by=sort_on, order_reverse=sort_reverse)]
        return Batch(log, b_size, b_start)

    def __call__(self):
        context = aq_inner(self.context)
        tracked = contentIsTracked(context) is not None
        directlytracked = self.isdirectlytracked()

        if self.request.get('enable', None) is not None and not directlytracked:
            alsoProvides(context, IContentIsTracked)
        elif self.request.get('disable', None) is not None and directlytracked:
            noLongerProvides(context, IContentIsTracked)

        # Avoid tracking the tracking view
        alsoProvides(self.request, IContentIsIgnored)
        return self.index()

from Acquisition import aq_inner
from zope.component import queryUtility
from zope.interface import alsoProvides, noLongerProvides
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from slc.clicktracker.interfaces import IClickStorage, IClickTrackerSettings
from slc.clicktracker.interfaces import IContentIsTracked
from slc.clicktracker.util import contentIsTracked
from slc.clicktracker import MessageFactory as _

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

    def __call__(self):
        context = aq_inner(self.context)
        tracked = contentIsTracked(context) is not None
        directlytracked = self.isdirectlytracked()

        if self.request.get('enable', None) is not None and not directlytracked:
            alsoProvides(context, IContentIsTracked)
        elif self.request.get('disable', None) is not None and directlytracked:
            noLongerProvides(context, IContentIsTracked)

        return self.index()

from zope.component import queryUtility
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from Products.Five import BrowserView
from slc.clicktracker.interfaces import IClickStorage, IClickTrackerSettings
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

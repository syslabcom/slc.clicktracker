from plone.app.layout.navigation.interfaces import INavigationRoot
from slc.clicktracker.interfaces import IContentIsTracked

def contentIsTracked(context):
    """ Check the whole tree until we hit INavigationRoot. When we find
        content that is tracked, return it. """
    while hasattr(context, 'aq_parent') and not INavigationRoot.providedBy(context):
        if IContentIsTracked.providedBy(context):
            return context
        context = context.aq_parent
    return None

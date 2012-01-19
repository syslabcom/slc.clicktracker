from Products.Five import BrowserView

class TrackerCallbackView(BrowserView):
    """ This is called via jquery POST. """
    def __call__(self):
        # TODO implement logging magic here
        return '' # No content

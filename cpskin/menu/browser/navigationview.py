from AccessControl import getSecurityManager
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import noLongerProvides

from cpskin.menu.interfaces import IForthLevelNavigation
from cpskin.menu.interfaces import IMultiLevelNavigationView


class MultiLevelNavigationView(BrowserView):
    """ Multi level navitation helper view
    """
    implements(IMultiLevelNavigationView)

    def _redirect(self, msg=''):
        """ Redirect
        """
        if self.request:
            if msg:
                IStatusMessage(self.request).addStatusMessage(msg, type='info')
            self.request.response.redirect(self.context.absolute_url())
        return msg

    def _get_real_context(self):
        context = self.context
        plone_view = getMultiAdapter((context, self.request), name="plone")
        if plone_view.isDefaultPageInFolder():
            context = aq_parent(context)
        context = aq_inner(context)
        return context

    @property
    def can_enable_forth_level(self):
        """ Helper method used by the actions to know if they should
        be displayed or not
        """
        context = self._get_real_context()

        sm = getSecurityManager()
        if not sm.checkPermission("Portlets: Manage portlets", context):
            return False

        depth = len(context.getPhysicalPath()[2:])
        if depth == 3 and not IForthLevelNavigation.providedBy(context):
            return True
        else:
            return False

    @property
    def can_disable_forth_level(self):
        """ Return True if the forth menu level is enable in this context
        """
        context = self._get_real_context()
        sm = getSecurityManager()
        if not sm.checkPermission("Portlets: Manage portlets", context):
            return False
        return IForthLevelNavigation.providedBy(context)

    def enable_forth_level(self):
        """ Enable the 4th level navigation """
        context = self._get_real_context()
        alsoProvides(context, IForthLevelNavigation)
        self._redirect()

    def disable_forth_level(self):
        """ Disable the 4th level navigation """
        context = self._get_real_context()
        noLongerProvides(context, IForthLevelNavigation)
        self._redirect()

    def __call__(self):
        return self.is_forth_level_nav_enabled(self.context)

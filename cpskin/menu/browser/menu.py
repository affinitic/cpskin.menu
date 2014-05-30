# -*- coding: utf-8 -*-
from zope.component import getMultiAdapter, queryUtility
from zope.globalrequest import getRequest
from affinitic.caching.memcached import invalidate_key

from Acquisition import aq_inner, aq_parent

from plone import api
from plone.app.layout.viewlets import common
from plone.app.layout.navigation.navtree import buildFolderTree

from lovely.memcached.interfaces import IMemcachedClient
from affinitic.caching import cache
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.CMFPlone.interfaces import IPloneSiteRoot

from cpskin.menu.interfaces import IDirectAccess

from zope.i18n import translate

from collective.superfish.browser.sections import (VirtualCatalogBrain,
                                                   SuperFishQueryBuilder,
                                                   SuperFishViewlet)


def cache_key(meth, viewlet):
    key = "menu.{0}".format(viewlet.navigation_root_path)
    return key


cached_method_id = 'cpskin.menu.browser.menu.superfish_portal_tabs'


def invalidate_menu_dependencies():
    if queryUtility(IMemcachedClient) is None:
        return  # functionality only available with memcached
    key = "{0}:{1}".format(
        cached_method_id,
        'menu')
    invalidate_key(cached_method_id, key)


def invalidate_menu(context):
    request = getRequest()
    if request is None:  # when plone site is created
        request = context.REQUEST
    viewlet = CpskinMenuViewlet(context, request, None, None)
    key = "{0}:{1}".format(
        cached_method_id,
        cache_key(viewlet.superfish_portal_tabs, viewlet))
    invalidate_key(cached_method_id, key)
    invalidate_menu_dependencies()


class CpskinMenuViewlet(common.GlobalSectionsViewlet, SuperFishViewlet):

    index = ViewPageTemplateFile('menu.pt')

    # monkey patch this if you want to use collective.superfish together with
    # global_sections, need another start level or menu depth.
    menu_id = 'portal-globalnav-cpskinmenu'
    menu_depth = 4

    ADD_PORTAL_TABS = True

    # this template is used to generate a single menu item.
    _menu_item = u"""<li id="%(menu_id)s-%(id)s"%(classnames)s><span%(selected)s><a href="%(url)s" title="%(description)s" id="%(id)s" tabindex="%(tabindex)s">%(title)s</a></span>%(submenu)s</li>"""

    # this template is used to generate a menu container
    _submenu_item = u"""<ul%(id)s class="%(classname)s">%(close)s%(menuitems)s</ul>"""

    def _get_real_context(self):
        context = self.context
        plone_view = getMultiAdapter((context, self.request), name="plone")
        if plone_view.isDefaultPageInFolder():
            context = aq_parent(context)
        context = aq_inner(context)
        return context

    @property
    def is_homepage(self):
        return IPloneSiteRoot.providedBy(self._get_real_context())

    def __init__(self, *args):
        super(CpskinMenuViewlet, self).__init__(*args)

        context_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_context_state')
        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')

        self.current_url = context_state.current_page_url()
        self.site_url = portal_state.portal_url()
        context = self._get_real_context()
        self.navigation_root_path = '/'.join(context.getPhysicalPath()[:3])
        self.mobile_navigation_root_path = portal_state.navigation_root_path()

    def _build_navtree(self, navigation_root, depth):
        # we generate our navigation out of the sitemap. so we can use the
        # highspeed navtree generation, and use it's caching features too.
        query = SuperFishQueryBuilder(self.context)()
        query['path']['depth'] = depth
        query['path']['query'] = navigation_root

        # no special strategy needed, so i kicked the INavtreeStrategy lookup.
        context = self._get_real_context()
        return buildFolderTree(self.context, obj=context, query=query)

    def update(self):
        super(CpskinMenuViewlet, self).update()
        # Why different depth in desktop and mobile?
        self.data = self._build_navtree(self.navigation_root_path,
                                        depth=self.menu_depth - 1)
        self.data_mobile = self._build_navtree(self.mobile_navigation_root_path,
                                               depth=self.menu_depth)

        if self.ADD_PORTAL_TABS and self.is_homepage:
            self._addActionsToData()

    @cache(cache_key, dependencies=['menu'])
    def superfish_portal_tabs(self):
        """We do not want to use the template-code any more.
           Python code should speedup rendering."""

        def submenu(items, tabindex, menu_level=0, menu_classnames='', close_button=False):
            i = 0
            s = []

            # exclude nav items
            items = [item for item in items if not item['item'].exclude_from_nav]

            if not items:
                return ''

            for item in items:
                first = (i == 0)
                i += 1
                last = (i == len(items))

                s.append(menuitem(item, tabindex, first, last, menu_level))

            menu_id = u""
            if self.menu_id:
                if not menu_level:
                    menu_id = self.menu_id and u" id=\"%s\"" % (self.menu_id) or u""

            submenu = u""
            close = u""
            if close_button and menu_level == 1:
                close = """<img src="++resource++cpskin.menu.resources/close.png" class="navTreeClose" />"""
            submenu = self._submenu_item % dict(
                id=menu_id,
                menuitems=u"".join(s),
                classname=u"navTreeLevel%d %s" % (
                    menu_level, menu_classnames),
                close=close,
            )
            return submenu

        def menuitem(item, tabindex, first=False, last=False, menu_level=0):
            classes = []

            if first:
                classes.append('firstItem')
            if last:
                classes.append('lastItem')
            if item['currentParent']:
                classes.append('navTreeItemInPath')

            brain = item['item']

            if type(brain) == VirtualCatalogBrain:
                # translate our portal_actions and use their id instead of the
                # url
                title = translate(brain.Title, context=self.request)
                desc = translate(brain.Description, context=self.request)
                item_id = brain.id
            else:
                title = safe_unicode(brain.Title)
                desc = safe_unicode(brain.Description)
                item_id = brain.getURL()[len(self.site_url):]

            item_id = item_id.strip('/').replace('/', '-')

            children = item['children']

            if self.mobile:
                direct_access_level = 1
                fourth_menu_level = 2
            else:
                direct_access_level = self.is_homepage and 1 or 0
                fourth_menu_level = self.is_homepage and 2 or 1

            if menu_level == direct_access_level:
                queryDict = {}
                queryDict['path'] = {'query': item['item'].getPath(), 'depth': 10}
                queryDict['object_provides'] = 'cpskin.menu.interfaces.IDirectAccess'
                catalog = getToolByName(self.context, 'portal_catalog')

                direct_access_catalog = catalog(queryDict)
                direct_access = []
                normal_children = []
                for child in children:
                    normal_children.append(child)
                for element in direct_access_catalog:
                    direct_access.append({'item': element,
                                          'depth': 1,
                                          'children': [],
                                          'currentParent': False,
                                          'currentItem': False})
                if direct_access:
                    submenu_render = submenu(
                        normal_children,
                        tabindex,
                        menu_level=menu_level + 1,
                        menu_classnames='has_direct_access',
                        close_button=False) or u""
                    submenu_render += submenu(
                        direct_access,
                        tabindex,
                        menu_level=menu_level + 1,
                        menu_classnames='direct_access',
                        close_button=True) or u""
                else:
                    submenu_render = submenu(
                        children,
                        tabindex,
                        menu_level=menu_level + 1,
                        menu_classnames='no_direct_access',
                        close_button=True) or u""
            elif menu_level == fourth_menu_level:
                if IDirectAccess.providedBy(item['item'].getObject()):
                    submenu_render = u""
                else:
                    helper_view = getMultiAdapter((item['item'].getObject(), self.request), name=u'multilevel-navigation')
                    if helper_view.is_enabled:
                        submenu_render = submenu(
                            children,
                            tabindex,
                            menu_level=menu_level + 1,
                            close_button=True) or u""
                    else:
                        submenu_render = u""
            else:
                submenu_render = submenu(
                    children,
                    tabindex,
                    menu_level=menu_level + 1,
                    close_button=True) or u""

            return self._menu_item % dict(
                menu_id=self.menu_id,
                id=item_id,
                tabindex=tabindex,
                level=menu_level,
                title=self.html_escape(title),
                description=self.html_escape(desc),
                url=item['item'].getURL(),
                classnames=len(classes) and u' class="%s"' % (" ".join(classes)) or u"",
                selected=item['currentItem'] and u' class="selected"' or u"",
                submenu=submenu_render)

        menus = {}

        self.mobile = False
        self.menu_id = 'portal-globalnav-cpskinmenu'

        tabindex = self._calculate_tabindex()

        # We do not need to calculate menu if not in a theme view
        if self.data and self._is_in_theme:
            menus['desktop'] = submenu(
                self.data['children'],
                tabindex,
                menu_classnames=u"sf-menu",
                close_button=True,
            )
        self.mobile = True
        self.menu_id = 'portal-globalnav-cpskinmenu-mobile'
        if self.data_mobile:
            menus['mobile'] = submenu(
                self.data_mobile['children'],
                tabindex,
                menu_classnames=u"sf-menu-mobile",
                close_button=False,
            )
        return menus

    def _calculate_tabindex(self):
        """
        Calculate tabindex of actual context
        """
        navigation_root = getNavigationRoot(self.context)
        tabindex = 1
        for brain in navigation_root:
            menu_object = brain.getObject()
            if menu_object == self.context:
                break
            tabindex += 1
        return tabindex

    def _is_in_theme(self):
        """
        Returns True if we are currently in a theme (non root, navigation view)
        """
        context = self.context
        # Get the right object if we are on a default page
        portal = getToolByName(context, 'portal_url').getPortalObject()
        plone_view = portal.restrictedTraverse('@@plone')
        if plone_view.isDefaultPageInFolder():
            # if the context is a default page, get the parent!
            obj = context.aq_inner.aq_parent
            context = obj
        # Take the path, traverse to the first level and see if it is a
        # element respecting the navigation strategy
        portal_url = getToolByName(context, 'portal_url')
        contentPath = portal_url.getRelativeContentPath(context)
        if not len(contentPath):
            # we are on the home page
            return False
        # Use the portal_catalog the get the first level element
        portal_catalog = getToolByName(context, 'portal_catalog')
        portal = getToolByName(context, 'portal_url').getPortalObject()
        queryDict = {}
        queryDict['path'] = {'query': '/'.join(portal.getPhysicalPath()) + '/' + contentPath[0], 'depth': 0}
        queryDict['portal_type'] = 'Folder'
        brains = portal_catalog(queryDict)
        if not brains:
            return False
        brain = brains[0]
        navtreeProps = getToolByName(context, 'portal_properties').navtree_properties
        if not brain.meta_type in navtreeProps.metaTypesNotToList and \
           (brain.review_state in navtreeProps.wf_states_to_show or
            not navtreeProps.enable_wf_state_filtering) and \
           not brain.id in navtreeProps.idsNotToList:
            return True
        return False


def getNavigationRoot(context):
    """
    Return brains of the navigation root menu
    """
    # Get 1st level folders appearing in navigation
    portal_catalog = api.portal.get_tool('portal_catalog')
    navtreeProps = api.portal.get_tool('portal_properties').navtree_properties
    portal = api.portal.get()
    queryDict = {}
    # LATER : queryPath = getNavigationRoot(context) ?
    queryDict['path'] = {'query': '/'.join(portal.getPhysicalPath()), 'depth': 1}
    if navtreeProps.enable_wf_state_filtering:
        queryDict['review_state'] = navtreeProps.wf_states_to_show
    queryDict['sort_on'] = 'getObjPositionInParent'
    queryDict['portal_type'] = 'Folder'
    queryDict['is_default_page'] = False
    brains = portal_catalog(queryDict)
    res = [b for b in brains if b.id not in navtreeProps.idsNotToList]
    return res

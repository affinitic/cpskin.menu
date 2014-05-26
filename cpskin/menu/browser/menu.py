# -*- coding: utf-8 -*-
from zope.component import getMultiAdapter

from Acquisition import aq_inner, aq_parent

from plone.app.layout.viewlets import common
from plone.app.layout.navigation.navtree import buildFolderTree

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.CMFPlone.interfaces import IPloneSiteRoot

from cpskin.menu.interfaces import IDirectAccess

from zope.i18n import translate

from collective.superfish.browser.sections import (VirtualCatalogBrain,
                                                   SuperFishQueryBuilder,
                                                   SuperFishViewlet)


class CpskinMenuViewlet(common.GlobalSectionsViewlet, SuperFishViewlet):

    index = ViewPageTemplateFile('menu.pt')

    # monkey patch this if you want to use collective.superfish together with
    # global_sections, need another start level or menu depth.
    menu_id = 'portal-globalnav-cpskinmenu'
    menu_depth = 4

    ADD_PORTAL_TABS = True

    # this template is used to generate a single menu item.
    _menu_item = u"""<li id="%(menu_id)s-%(id)s"%(classnames)s><span%(selected)s><a href="%(url)s" title="%(description)s" id="%(id)s">%(title)s</a></span>%(submenu)s</li>"""

    # this template is used to generate a menu container
    _submenu_item = u"""<ul%(id)s class="%(classname)s">%(menuitems)s</ul>"""

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

    def superfish_portal_tabs(self):
        """We do not want to use the template-code any more.
           Python code should speedup rendering."""

        def submenu(items, menu_level=0, menu_classnames=''):

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

                s.append(menuitem(item, first, last, menu_level))

            menu_id = u""
            if self.menu_id:
                if not menu_level:
                    menu_id = self.menu_id and u" id=\"%s\"" % (self.menu_id) or u""

            return self._submenu_item % dict(
                id=menu_id,
                menuitems=u"".join(s),
                classname=u"navTreeLevel%d %s" % (
                    menu_level, menu_classnames)
            )

        def menuitem(item, first=False, last=False, menu_level=0):
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
                        menu_level=menu_level + 1,
                        menu_classnames='has_direct_access') or u""
                    submenu_render += submenu(
                        direct_access,
                        menu_level=menu_level + 1,
                        menu_classnames='direct_access') or u""
                else:
                    submenu_render = submenu(
                        children,
                        menu_level=menu_level + 1,
                        menu_classnames='no_direct_access') or u""
            elif menu_level == fourth_menu_level:
                if IDirectAccess.providedBy(item['item'].getObject()):
                    submenu_render = u""
                else:
                    helper_view = getMultiAdapter((item['item'].getObject(), self.request), name=u'multilevel-navigation')
                    if helper_view.is_enabled:
                        submenu_render = submenu(
                            children,
                            menu_level=menu_level + 1) or u""
                    else:
                        submenu_render = u""
            else:
                submenu_render = submenu(
                    children,
                    menu_level=menu_level + 1) or u""

            return self._menu_item % dict(
                menu_id=self.menu_id,
                id=item_id,
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
        if self.data:
            menus['desktop'] = submenu(
                self.data['children'],
                menu_classnames=u"sf-menu"
            )
        self.mobile = True
        self.menu_id = 'portal-globalnav-cpskinmenu-mobile'
        if self.data_mobile:
            menus['mobile'] = submenu(
                self.data_mobile['children'],
                menu_classnames=u"sf-menu-mobile"
            )
        return menus

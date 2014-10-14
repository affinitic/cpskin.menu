# -*- coding: utf-8 -*-
import unittest2 as unittest
from zope.component import getUtility
from zope.ramcache.interfaces.ram import IRAMCache
from plone.uuid.interfaces import IUUID
from plone import api
from cpskin.menu.testing import CPSKIN_MENU_LOAD_PAGE_INTEGRATION_TESTING
from cpskin.menu.browser.menu import (CpskinMenuViewlet, cache_key,
                                      invalidate_menu)


def get_cache_miss():
    storage = getUtility(IRAMCache)._getStorage()
    return storage._misses.get('cpskin.menu.browser.menu.superfish_portal_tabs', 0)


class TestMenu(unittest.TestCase):

    layer = CPSKIN_MENU_LOAD_PAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_menu_portal_tabs(self):
        viewlet = CpskinMenuViewlet(self.portal, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.is_homepage)
        menus = viewlet.superfish_portal_tabs()
        self.assertEqual(len(menus), 2)

    def test_menu_cache_key_on_root(self):
        viewlet = CpskinMenuViewlet(self.portal, self.request, None, None)
        viewlet.update()
        key = cache_key(viewlet.superfish_portal_tabs, viewlet)
        self.assertTrue(key.startswith('menu.'))
        self.assertTrue(key.endswith(IUUID(self.portal)))

    def test_menu_cache_key_on_communes(self):
        communes = getattr(self.portal, 'commune')
        viewlet = CpskinMenuViewlet(communes, self.request, None, None)
        viewlet.update()
        key = cache_key(viewlet.superfish_portal_tabs, viewlet)
        self.assertTrue(key.startswith('menu.'))
        self.assertTrue(key.endswith(IUUID(communes)))

    def test_menu_cache_key_on_communes_subitem(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        communes = getattr(self.portal, 'commune')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        key = cache_key(viewlet.superfish_portal_tabs, viewlet)
        self.assertTrue(key.startswith('menu.'))
        self.assertTrue(key.endswith(IUUID(communes)))

    def test_menu_cache_usage_test_fail(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(get_cache_miss(), 0)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)

    def test_menu_cache_usage_calculate_once(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(get_cache_miss(), 0)

        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)

        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)

        item = self.portal.restrictedTraverse('commune')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)

        item = self.portal.restrictedTraverse('loisirs')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 2)

    def test_menu_cache_invalidation(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(get_cache_miss(), 0)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)
        invalidate_menu(item)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 2)

    def test_menu_cache_invalidate_another_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        commune = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()

        self.assertEqual(get_cache_miss(), 0)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)

        loisirs = self.portal.restrictedTraverse('loisirs')
        invalidate_menu(loisirs)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)

        invalidate_menu(commune)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 2)

    def test_objet_modification_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(get_cache_miss(), 0)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)
        item.setTitle('Test Cache Invalidation')
        item.processForm()
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 2)

    def test_object_creation_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(get_cache_miss(), 0)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)
        api.content.create(item, 'Folder', 'foo')
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 2)

    def test_object_publication_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        self.assertEqual(get_cache_miss(), 0)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)
        api.content.transition(item, 'publish')
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 2)

    def test_object_removed_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        commune = self.portal.restrictedTraverse('commune')
        viewlet = CpskinMenuViewlet(commune, self.request, None, None)
        viewlet.update()
        self.assertEqual(get_cache_miss(), 0)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)
        api.content.delete(item)
        viewlet.update()
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 2)

    def test_object_moved_invalidates_menus(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        commune = self.portal.restrictedTraverse('commune')
        loisirs = self.portal.restrictedTraverse('loisirs')
        viewlet = CpskinMenuViewlet(commune, self.request, None, None)
        viewlet.update()
        self.assertEqual(get_cache_miss(), 0)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)
        viewlet_loisirs = CpskinMenuViewlet(loisirs, self.request, None, None)
        viewlet_loisirs.update()
        self.assertEqual(get_cache_miss(), 1)
        viewlet_loisirs.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 2)
        viewlet_loisirs.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 2)
        api.content.move(item, loisirs)
        viewlet.update()
        viewlet_loisirs.update()
        self.assertEqual(get_cache_miss(), 2)
        viewlet_loisirs.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 3)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 4)

    def test_object_rename_invalidates_menu(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        commune = self.portal.restrictedTraverse('commune')
        viewlet = CpskinMenuViewlet(commune, self.request, None, None)
        viewlet.update()
        self.assertEqual(get_cache_miss(), 0)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 1)
        api.content.rename(item, new_id='sc')
        viewlet.update()
        viewlet.superfish_portal_tabs()
        self.assertEqual(get_cache_miss(), 2)

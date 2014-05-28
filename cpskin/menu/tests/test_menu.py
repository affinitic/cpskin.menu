# -*- coding: utf-8 -*-
import unittest2 as unittest
from zope.component import getUtility
from zope.ramcache.interfaces.ram import IRAMCache
from cpskin.menu.testing import CPSKIN_MENU_INTEGRATION_TESTING
from cpskin.menu.browser.menu import (CpskinMenuViewlet, cache_key,
                                      invalidate_menu)


def get_cache_miss():
    storage = getUtility(IRAMCache)._getStorage()
    return storage._misses.get('cpskin.menu.browser.menu.superfish_portal_tabs', 0)


class TestMenu(unittest.TestCase):

    layer = CPSKIN_MENU_INTEGRATION_TESTING

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
        self.assertTrue(key.endswith('/plone'))

    def test_menu_cache_key_on_communes(self):
        communes = getattr(self.portal, 'commune')
        viewlet = CpskinMenuViewlet(communes, self.request, None, None)
        viewlet.update()
        key = cache_key(viewlet.superfish_portal_tabs, viewlet)
        self.assertTrue(key.startswith('menu.'))
        self.assertTrue(key.endswith('/plone/commune'))

    def test_menu_cache_key_on_communes_subitem(self):
        item = self.portal.restrictedTraverse('commune/services_communaux')
        viewlet = CpskinMenuViewlet(item, self.request, None, None)
        viewlet.update()
        key = cache_key(viewlet.superfish_portal_tabs, viewlet)
        self.assertTrue(key.startswith('menu.'))
        self.assertTrue(key.endswith('/plone/commune'))

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

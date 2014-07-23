# -*- coding: utf-8 -*-

from cpskin.menu import testing
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest


class TestVocabulary(unittest.TestCase):
    layer = testing.CPSKIN_MENU_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_vocabulary(self):
        factory = getUtility(IVocabularyFactory,
                             'cpskin.menu.vocabularies.lastlevelnavigation')
        voc = factory(self.portal)
        expected_values = [u'Promenades', u'Bibliothèques', u'Yoyo', u'Tata',
                           u'Rockers', u'Cinema', u'Abba', u'Finances']
        self.assertListEqual(expected_values, [t.title for t in voc])

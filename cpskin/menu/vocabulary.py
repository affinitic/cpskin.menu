# -*- coding: utf-8 -*-

from binascii import b2a_qp
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from plone import api
from Products.CMFPlone.utils import safe_unicode
from cpskin.menu.interfaces import IFourthLevelNavigation


def safe_encode(term):
    if isinstance(term, unicode):
        # no need to use portal encoding for transitional encoding from
        # unicode to ascii. utf-8 should be fine.
        term = term.encode('utf-8')
    return term


class LastLevelMenuVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context, query=None):
        portal = api.portal.get()
        brains = portal.portal_catalog(portal_type='Folder',
                                       review_state=('published_and_shown', ))

        result = [(b.getPath(), b.getObject()) for b in brains]
        filtered_result = [(p, o) for p, o in sorted(result, reverse=True)
                           if self.is_last_level(p, o)]
        items = [
            SimpleTerm(p, b2a_qp(safe_encode(o.title)), safe_unicode(o.title))
            for p, o in filtered_result
            if query is None or safe_encode(query) in safe_encode(o.title)
        ]

        return SimpleVocabulary(items)

    def is_last_level(self, path, obj):
        paths = path.split('/')[1:]
        if len(paths) == 4 and not IFourthLevelNavigation.providedBy(obj):
            return True
        elif len(paths) == 5:
            if IFourthLevelNavigation.providedBy(obj.aq_parent):
                return True
        return False


LastLevelMenuVocabularyFactory = LastLevelMenuVocabulary()

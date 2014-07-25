# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import safe_unicode
from binascii import b2a_qp
from cpskin.menu.interfaces import IFourthLevelNavigation
from plone import api
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def safe_encode(term):
    if isinstance(term, unicode):
        # no need to use portal encoding for transitional encoding from
        # unicode to ascii. utf-8 should be fine.
        term = term.encode('utf-8')
    return term


class LastLevelMenuVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context, query=None):
        self.context = context
        result = [(b.getObject(), b.getPath()) for b in self.get_brains()]
        filtered_result = [(o.title, p) for o, p
                           in sorted(result, reverse=True)
                           if self.is_last_level(p, o)]
        sorted_result = sorted(filtered_result)
        items = [
            SimpleTerm(path, b2a_qp(safe_encode(path)), safe_unicode(title))
            for title, path in sorted_result
            if query is None or safe_encode(query) in safe_encode(title)
        ]

        return SimpleVocabulary(items)

    def is_last_level(self, path, obj):
        paths = path.split('/')[1:]
        min_lvl, max_lvl = self.get_min_max_lvl()
        if len(paths) == min_lvl and not IFourthLevelNavigation.providedBy(obj):
            return True
        elif len(paths) == max_lvl:
            if IFourthLevelNavigation.providedBy(obj.aq_parent):
                return True
        return False

    def get_min_max_lvl(self):
        root_path = api.portal.get().getPhysicalPath()
        return (len(root_path) + 2, len(root_path) + 3)

    def get_brains(self):
        catalog = api.portal.get_tool('portal_catalog')
        navtree_props = api.portal.get_tool('portal_properties').navtree_properties
        portal = api.portal.get()

        query_dict = {'path': {'query': '/'.join(portal.getPhysicalPath()),
                               'depth': 4},
                      'portal_type': 'Folder',
                      'is_default_page': False}
        if navtree_props.enable_wf_state_filtering:
            query_dict['review_state'] = navtree_props.wf_states_to_show

        brains = catalog(query_dict)
        return [b for b in brains if b.id not in navtree_props.idsNotToList]


LastLevelMenuVocabularyFactory = LastLevelMenuVocabulary()

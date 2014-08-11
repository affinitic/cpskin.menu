# -*- coding: utf-8 -*-
from zope.component.hooks import getSite
from Acquisition import aq_chain
from plone.uuid.interfaces import IUUID
from cpskin.menu.browser.menu import invalidate_menu


def content_has_id(content):
    try:
        content.getId()
    except AttributeError:
        return False
    else:
        return True


def object_is_wrapped(content):
    return len(aq_chain(content)) > 1


def content_modified(content, event):
    if not content_has_id(content):
        return
    if not object_is_wrapped(content):
        return
    if IUUID(getSite(), None) is not None:
        invalidate_menu(content)

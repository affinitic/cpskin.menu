# -*- coding: utf-8 -*-
from zope.component.hooks import getSite
from plone.uuid.interfaces import IUUID
from cpskin.menu.browser.menu import invalidate_menu


def content_modified(content, event):
    if IUUID(getSite(), None) is not None:
        invalidate_menu(content)

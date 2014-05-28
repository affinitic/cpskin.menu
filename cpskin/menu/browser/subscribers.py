# -*- coding: utf-8 -*-
from cpskin.menu.browser.menu import invalidate_menu


def content_modified(content, event):
    invalidate_menu(content)

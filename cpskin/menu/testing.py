# -*- coding: utf-8 -*-

from plone.testing import z2
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneWithPackageLayer
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE

import cpskin.menu


CPSKIN_MENU_FIXTURE = PloneWithPackageLayer(
    name="CPSKIN_MENU_FIXTURE",
    zcml_filename="configure.zcml",
    zcml_package=cpskin.menu)


CPSKIN_MENU_ROBOT_TESTING = FunctionalTesting(
    bases=(CPSKIN_MENU_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="cpskin.menu:Robot")

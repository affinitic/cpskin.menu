# -*- coding: utf-8 -*-

from plone import api
from plone.testing import z2
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import applyProfile
from plone.app.testing import (login,
                               TEST_USER_NAME,
                               setRoles,
                               TEST_USER_ID)
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE

import cpskin.menu


class CPSkinMenuPloneWithPackageLayer(PloneWithPackageLayer):
    """
    plone (portal root)
    |-- Commune
    `-- Loisirs
        |-- Tourisme
        `-- Art & Culture
            |-- Bibliothèques
            `-- Artistes
                |-- Tata
                `-- Yoyo
    """

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'cpskin.menu:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        api.content.create(
            type='Folder',
            title='COMMUNE',
            id='commune',
            container=portal)
        loisirs = api.content.create(
            type='Folder',
            title='LOISIRS',
            id='loisirs',
            container=portal)
        api.content.create(
            type='Folder',
            title='Tourisme',
            id='tourisme',
            container=loisirs)
        art_et_culture = api.content.create(
            type='Folder',
            title='Art & Culture',
            id='art_et_culture',
            container=loisirs)
        api.content.create(
            type='Folder',
            title='Bibliothèques',
            id='bibliotheques',
            container=art_et_culture)
        artistes = api.content.create(
            type='Folder',
            title='Artistes',
            id='artistes',
            container=art_et_culture)
        api.content.create(
            type='Folder',
            title='Tata',
            id='tata',
            container=artistes)
        api.content.create(
            type='Folder',
            title='Yoyo',
            id='yoyo',
            container=artistes)


CPSKIN_MENU_FIXTURE = CPSkinMenuPloneWithPackageLayer(
    name="CPSKIN_MENU_FIXTURE",
    zcml_filename="configure.zcml",
    zcml_package=cpskin.menu)


CPSKIN_MENU_ROBOT_TESTING = FunctionalTesting(
    bases=(CPSKIN_MENU_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="cpskin.menu:Robot")

# -*- coding: utf-8 -*-
from plone.testing import layered
from cpskin.menu.testing import CPSKIN_MENU_ROBOT_TESTING_LOAD_PAGE

import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('robot_load_page/test_mobile.robot'),
                layer=CPSKIN_MENU_ROBOT_TESTING_LOAD_PAGE),
    ])
    return suite

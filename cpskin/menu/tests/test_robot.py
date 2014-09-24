# -*- coding: utf-8 -*-
from plone.testing import layered
from cpskin.menu.testing import CPSKIN_MENU_ROBOT_TESTING

import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('robot/test_direct_access.robot'),
                layer=CPSKIN_MENU_ROBOT_TESTING),
    ])
    return suite

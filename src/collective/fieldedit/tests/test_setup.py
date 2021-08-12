# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.fieldedit.testing import COLLECTIVE_FIELDEDIT_INTEGRATION_TESTING
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.fieldedit is properly installed."""

    layer = COLLECTIVE_FIELDEDIT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if collective.fieldedit is installed."""
        self.assertTrue(self.installer.is_product_installed("collective.fieldedit"))

    def test_browserlayer(self):
        """Test that ICollectiveFieldeditLayer is registered."""
        from collective.fieldedit.interfaces import ICollectiveFieldeditLayer
        from plone.browserlayer import utils

        self.assertIn(ICollectiveFieldeditLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_FIELDEDIT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        self.installer.uninstall_product("collective.fieldedit")

    def test_product_uninstalled(self):
        """Test if collective.fieldedit is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("collective.fieldedit"))

    def test_browserlayer_removed(self):
        """Test that ICollectiveFieldeditLayer is removed."""
        from collective.fieldedit.interfaces import ICollectiveFieldeditLayer
        from plone.browserlayer import utils

        self.assertNotIn(ICollectiveFieldeditLayer, utils.registered_layers())

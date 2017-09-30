# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from collective.fieldedit.testing import COLLECTIVE_FIELDEDIT_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.fieldedit is properly installed."""

    layer = COLLECTIVE_FIELDEDIT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.fieldedit is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.fieldedit'))

    def test_browserlayer(self):
        """Test that ICollectiveFieldeditLayer is registered."""
        from collective.fieldedit.interfaces import (
            ICollectiveFieldeditLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveFieldeditLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_FIELDEDIT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.fieldedit'])

    def test_product_uninstalled(self):
        """Test if collective.fieldedit is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.fieldedit'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveFieldeditLayer is removed."""
        from collective.fieldedit.interfaces import \
            ICollectiveFieldeditLayer
        from plone.browserlayer import utils
        self.assertNotIn(
           ICollectiveFieldeditLayer,
           utils.registered_layers())

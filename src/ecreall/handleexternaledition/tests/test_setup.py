# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from ecreall.handleexternaledition.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of ecreall.handleexternaledition into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ecreall.handleexternaledition is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('ecreall.handleexternaledition'))

    def test_uninstall(self):
        """Test if ecreall.handleexternaledition is cleanly uninstalled."""
        self.installer.uninstallProducts(['ecreall.handleexternaledition'])
        self.assertFalse(self.installer.isProductInstalled('ecreall.handleexternaledition'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IEcreallHandleexternaleditionLayer is registered."""
        from ecreall.handleexternaledition.interfaces import IEcreallHandleexternaleditionLayer
        from plone.browserlayer import utils
        self.assertIn(IEcreallHandleexternaleditionLayer, utils.registered_layers())

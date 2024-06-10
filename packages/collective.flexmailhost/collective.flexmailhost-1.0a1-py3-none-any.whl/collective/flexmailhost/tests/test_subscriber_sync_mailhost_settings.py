# -*- coding: utf-8 -*-
from collective.flexmailhost.testing import COLLECTIVE_FLEXMAILHOST_FUNCTIONAL_TESTING
from collective.flexmailhost.testing import COLLECTIVE_FLEXMAILHOST_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class SubscriberIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_FLEXMAILHOST_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])


class SubscriberFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_FLEXMAILHOST_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing import z2

import collective.fieldedit


class CollectiveFieldeditLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.fieldedit)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.fieldedit:default')
        portal.acl_users.userFolderAddUser(
            SITE_OWNER_NAME, SITE_OWNER_PASSWORD, ['Manager'], [])


COLLECTIVE_FIELDEDIT_FIXTURE = CollectiveFieldeditLayer()


COLLECTIVE_FIELDEDIT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_FIELDEDIT_FIXTURE,),
    name='CollectiveFieldeditLayer:IntegrationTesting'
)


COLLECTIVE_FIELDEDIT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_FIELDEDIT_FIXTURE,),
    name='CollectiveFieldeditLayer:FunctionalTesting'
)


COLLECTIVE_FIELDEDIT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_FIELDEDIT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveFieldeditLayer:AcceptanceTesting'
)

# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import zest.emailhider


class ZestEmailhiderLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=zest.emailhider)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'zest.emailhider:default')


ZEST_EMAILHIDER_FIXTURE = ZestEmailhiderLayer()


ZEST_EMAILHIDER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ZEST_EMAILHIDER_FIXTURE,),
    name='ZestEmailhiderLayer:IntegrationTesting'
)


ZEST_EMAILHIDER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ZEST_EMAILHIDER_FIXTURE,),
    name='ZestEmailhiderLayer:FunctionalTesting'
)


ZEST_EMAILHIDER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        ZEST_EMAILHIDER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='ZestEmailhiderLayer:AcceptanceTesting'
)

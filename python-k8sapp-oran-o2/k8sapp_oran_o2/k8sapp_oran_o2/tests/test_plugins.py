#
# Copyright (c) 2022 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

from sysinv.common import constants
from sysinv.tests.db import base as dbbase
from sysinv.tests.helm.test_helm import HelmOperatorTestSuiteMixin


class K8SAppOrano2AppMixin(object):
    app_name = constants.HELM_APP_ORAN_O2
    path_name = app_name + '.tgz'

    def setUp(self):
        super(K8SAppOrano2AppMixin, self).setUp()


# Test Configuration:
# - Controller
# - IPv6
# - Ceph Storage
# - oran-o2 app
class K8sAppOrano2ControllerTestCase(K8SAppOrano2AppMixin,
                                      dbbase.BaseIPv6Mixin,
                                      dbbase.BaseCephStorageBackendMixin,
                                      HelmOperatorTestSuiteMixin,
                                      dbbase.ControllerHostTestCase):
    pass


# Test Configuration:
# - AIO
# - IPv4
# - Ceph Storage
# - oran-o2 app
class K8SAppOrano2AIOTestCase(K8SAppOrano2AppMixin,
                               dbbase.BaseCephStorageBackendMixin,
                               HelmOperatorTestSuiteMixin,
                               dbbase.AIOSimplexHostTestCase):
    pass

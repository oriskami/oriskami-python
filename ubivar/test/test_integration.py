# -*- coding: utf-8 -*-
import os
import sys
import unittest2
import ubivar

from mock import patch
from ubivar.test.helper import (UbivarTestCase, NOW)


class FunctionalTests(UbivarTestCase):
    request_client = ubivar.http_client.Urllib2Client

    def setUp(self):
        super(FunctionalTests, self).setUp()

        def get_http_client(*args, **kwargs):
            return self.request_client(*args, **kwargs)

        self.client_patcher = patch(
            'ubivar.http_client.new_default_http_client')

        client_mock = self.client_patcher.start()
        client_mock.side_effect = get_http_client

    def tearDown(self):
        super(FunctionalTests, self).tearDown()

        self.client_patcher.stop()


class RequestsFunctionalTests(FunctionalTests):
    request_client = ubivar.http_client.RequestsClient


if __name__ == '__main__':
    unittest2.main()

import datetime
import os
import random
import string
import sys
import unittest2

from mock import patch, Mock

import ubivar 

NOW = datetime.datetime.now()


SAMPLE_INVOICE = ubivar.util.json.loads("""
{
  "amount_due": 1305,
  "attempt_count": 0,
  "attempted": true,
  "charge": "ch_wajkQ5aDTzFs5v",
  "closed": true,
  "customer": "cus_osllUe2f1BzrRT",
  "date": 1338238728,
  "discount": null,
  "ending_balance": 0,
  "id": "in_t9mHb2hpK7mml1",
  "livemode": false,
  "next_payment_attempt": null,
  "object": "invoice",
  "paid": true,
  "period_end": 1338238728,
  "period_start": 1338238716,
  "starting_balance": -8695,
  "subtotal": 10000,
  "total": 10000,
  "lines": {
    "invoiceitems": [],
    "prorations": [],
    "subscriptions": [
      {
        "plan": {
          "interval": "month",
          "object": "plan",
          "identifier": "expensive",
          "currency": "usd",
          "livemode": false,
          "amount": 10000,
          "name": "Expensive Plan",
          "trial_period_days": null,
          "id": "expensive"
        },
        "period": {
          "end": 1340917128,
          "start": 1338238728
        },
        "amount": 10000
      }
    ]
  }
}
""")

DUMMY_WEBHOOK_PAYLOAD = """{
  "id": "evt_test_webhook",
  "object": "event"
}"""

DUMMY_WEBHOOK_SECRET = 'whsec_test_secret'


class UbivarTestCase(unittest2.TestCase):
    RESTORE_ATTRIBUTES = ('api_version', 'api_key', 'client_id')

    def setUp(self):
        super(UbivarTestCase, self).setUp()

        self._ubivar_original_attributes = {}

        for attr in self.RESTORE_ATTRIBUTES:
            self._ubivar_original_attributes[attr] = getattr(ubivar, attr)

        api_base = os.environ.get('STRIPE_API_BASE')
        if api_base:
            ubivar.api_base = api_base
        ubivar.api_key = os.environ.get(
            'STRIPE_API_KEY', 'tGN0bIwXnHdwOa85VABjPdSn8nWY7G7I')
        ubivar.api_version = os.environ.get(
            'STRIPE_API_VERSION', '2017-04-06')

    def tearDown(self):
        super(UbivarTestCase, self).tearDown()

        for attr in self.RESTORE_ATTRIBUTES:
            setattr(ubivar, attr, self._ubivar_original_attributes[attr])


class UbivarUnitTestCase(UbivarTestCase):
    REQUEST_LIBRARIES = ['urlfetch', 'requests', 'pycurl']

    if sys.version_info >= (3, 0):
        REQUEST_LIBRARIES.append('urllib.request')
    else:
        REQUEST_LIBRARIES.append('urllib2')

    def setUp(self):
        super(UbivarUnitTestCase, self).setUp()

        self.request_patchers = {}
        self.request_mocks = {}
        for lib in self.REQUEST_LIBRARIES:
            patcher = patch("ubivar.http_client.%s" % (lib,))

            self.request_mocks[lib] = patcher.start()
            self.request_patchers[lib] = patcher

    def tearDown(self):
        super(UbivarUnitTestCase, self).tearDown()

        for patcher in self.request_patchers.itervalues():
            patcher.stop()


class UbivarAPIRequestorTestCase(UbivarUnitTestCase):
    REQUESTOR_CLS = ubivar.api_requestor.APIRequestor

    def setUp(self):
        super(UbivarAPIRequestorTestCase, self).setUp()

        self.http_client = Mock(ubivar.http_client.HTTPClient)
        self.http_client._verify_ssl_certs = True
        self.http_client.name = 'mockclient'

        self.requestor = self.REQUESTOR_CLS(client=self.http_client)

    def mock_response(self, return_body, return_code, requestor=None,
                      headers=None):
        if not requestor:
            requestor = self.requestor

        self.http_client.request = Mock(
            return_value=(return_body, return_code, headers or {}))


class UbivarOAuthRequestorTestCase(UbivarAPIRequestorTestCase):
    REQUESTOR_CLS = ubivar.api_requestor.OAuthRequestor


class UbivarApiTestCase(UbivarTestCase):
    REQUESTOR_CLS_NAME = 'ubivar.api_requestor.APIRequestor'

    def setUp(self):
        super(UbivarApiTestCase, self).setUp()

        self.requestor_patcher = patch(self.REQUESTOR_CLS_NAME)
        requestor_class_mock = self.requestor_patcher.start()
        self.requestor_mock = requestor_class_mock.return_value

    def tearDown(self):
        super(UbivarApiTestCase, self).tearDown()

        self.requestor_patcher.stop()

    def mock_response(self, res):
        self.requestor_mock.request = Mock(return_value=(res, 'reskey'))


class UbivarOAuthTestCase(UbivarApiTestCase):
    REQUESTOR_CLS_NAME = 'ubivar.api_requestor.OAuthRequestor'

    def setUp(self):
        super(UbivarOAuthTestCase, self).setUp()
        self.mock_response({})


class UbivarResourceTest(UbivarApiTestCase):

    def setUp(self):
        super(UbivarResourceTest, self).setUp()
        self.mock_response({})


class MyResource(ubivar.resource.APIResource):
    pass


class MySingleton(ubivar.resource.SingletonAPIResource):
    pass


class MyListable(ubivar.resource.ListableAPIResource):
    pass


class MyCreatable(ubivar.resource.CreateableAPIResource):
    pass


class MyUpdateable(ubivar.resource.UpdateableAPIResource):
    pass


class MyDeletable(ubivar.resource.DeletableAPIResource):
    pass


class MyComposite(ubivar.resource.ListableAPIResource,
                  ubivar.resource.CreateableAPIResource,
                  ubivar.resource.UpdateableAPIResource,
                  ubivar.resource.DeletableAPIResource):
    pass

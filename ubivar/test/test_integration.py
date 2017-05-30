# -*- coding: utf-8 -*-
import os
import sys
import unittest2
import ubivar

from mock import patch
from ubivar.test.helper import (UbivarTestCase, NOW, DUMMY_CHARGE, DUMMY_CARD)


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

    def test_dns_failure(self):
        api_base = ubivar.api_base
        try:
            ubivar.api_base = 'https://my-invalid-domain.ireallywontresolve/v1'
            self.assertRaises(ubivar.error.APIConnectionError,
                              ubivar.Customer.create)
        finally:
            ubivar.api_base = api_base

    def test_run(self):
        charge = ubivar.Charge.create(**DUMMY_CHARGE)
        self.assertFalse(charge.refunded)
        charge.refund()
        self.assertTrue(charge.refunded)

    def test_refresh(self):
        charge = ubivar.Charge.create(**DUMMY_CHARGE)
        charge2 = ubivar.Charge.retrieve(charge.id)
        self.assertEqual(charge2.created, charge.created)

        charge2.junk = 'junk'
        charge2.refresh()
        self.assertRaises(AttributeError, lambda: charge2.junk)

    def test_list_accessors(self):
        customer = ubivar.Customer.create(card=DUMMY_CARD)
        self.assertEqual(customer['created'], customer.created)
        customer['foo'] = 'bar'
        self.assertEqual(customer.foo, 'bar')

    def test_raise(self):
        EXPIRED_CARD = DUMMY_CARD.copy()
        EXPIRED_CARD['exp_month'] = NOW.month - 2
        EXPIRED_CARD['exp_year'] = NOW.year - 2
        self.assertRaises(ubivar.error.CardError, ubivar.Charge.create,
                          amount=100, currency='usd', card=EXPIRED_CARD)

    def test_response_headers(self):
        EXPIRED_CARD = DUMMY_CARD.copy()
        EXPIRED_CARD['exp_month'] = NOW.month - 2
        EXPIRED_CARD['exp_year'] = NOW.year - 2
        try:
            ubivar.Charge.create(amount=100, currency='usd', card=EXPIRED_CARD)
            self.fail('charge creation with expired card did not fail')
        except ubivar.error.CardError as e:
            self.assertTrue(e.request_id.startswith('req_'))

    def test_unicode(self):
        # Make sure unicode requests can be sent
        self.assertRaises(ubivar.error.InvalidRequestError,
                          ubivar.Charge.retrieve,
                          id=u'☃')

    def test_none_values(self):
        customer = ubivar.Customer.create(plan=None)
        self.assertTrue(customer.id)

    def test_missing_id(self):
        customer = ubivar.Customer()
        self.assertRaises(ubivar.error.InvalidRequestError, customer.refresh)


class RequestsFunctionalTests(FunctionalTests):
    request_client = ubivar.http_client.RequestsClient


class UrlfetchFunctionalTests(FunctionalTests):
    request_client = 'urlfetch'

    def setUp(self):
        if ubivar.http_client.urlfetch is None:
            self.skipTest(
                '`urlfetch` from Google App Engine is unavailable.')
        else:
            super(UrlfetchFunctionalTests, self).setUp()


class PycurlFunctionalTests(FunctionalTests):

    def setUp(self):
        if not os.environ.get('STRIPE_TEST_PYCURL'):
            self.skipTest('Pycurl skipped as STRIPE_TEST_PYCURL is not set')
        if sys.version_info >= (3, 0):
            self.skipTest('Pycurl is not supported in Python 3')
        else:
            super(PycurlFunctionalTests, self).setUp()

    request_client = ubivar.http_client.PycurlClient


class AuthenticationErrorTest(UbivarTestCase):

    def test_invalid_credentials(self):
        key = ubivar.api_key
        try:
            ubivar.api_key = 'invalid'
            ubivar.Customer.create()
        except ubivar.error.AuthenticationError as e:
            self.assertEqual(401, e.http_status)
            self.assertTrue(isinstance(e.http_body, basestring))
            self.assertTrue(isinstance(e.json_body, dict))
            # Note that an invalid API key bypasses many of the standard
            # facilities in the API server so currently no Request ID is
            # returned.
        finally:
            ubivar.api_key = key


class CardErrorTest(UbivarTestCase):

    def test_declined_card_props(self):
        EXPIRED_CARD = DUMMY_CARD.copy()
        EXPIRED_CARD['exp_month'] = NOW.month - 2
        EXPIRED_CARD['exp_year'] = NOW.year - 2
        try:
            ubivar.Charge.create(amount=100, currency='usd', card=EXPIRED_CARD)
        except ubivar.error.CardError as e:
            self.assertEqual(402, e.http_status)
            self.assertTrue(isinstance(e.http_body, basestring))
            self.assertTrue(isinstance(e.json_body, dict))
            self.assertTrue(e.request_id.startswith('req_'))


class InvalidRequestErrorTest(UbivarTestCase):

    def test_nonexistent_object(self):
        try:
            ubivar.Charge.retrieve('invalid')
        except ubivar.error.InvalidRequestError as e:
            self.assertEqual(404, e.http_status)
            self.assertTrue(isinstance(e.http_body, basestring))
            self.assertTrue(isinstance(e.json_body, dict))
            self.assertTrue(e.request_id.startswith('req_'))

    def test_invalid_data(self):
        try:
            ubivar.Charge.create()
        except ubivar.error.InvalidRequestError as e:
            self.assertEqual(400, e.http_status)
            self.assertTrue(isinstance(e.http_body, basestring))
            self.assertTrue(isinstance(e.json_body, dict))
            self.assertTrue(e.request_id.startswith('req_'))


if __name__ == '__main__':
    unittest2.main()

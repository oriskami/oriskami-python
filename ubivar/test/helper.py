import datetime
import os
import random
import string
import sys
import unittest2

from mock import patch, Mock

import ubivar

DUMMY_EVENT_1 = {
          "id"                          : "1"           # a unique id 
        , "email"                       : "abc@gmail.com"
        , "names"                       : "M Abc"
        , "account_creation_time"       : "2017-05-17 21:50:00"
        , "account_id"                  : "10"
        , "account_n_fulfilled"         : "1"
        , "account_total_since_created" : "49.40"
        , "account_total_cur"           : "EUR"
        , "invoice_time"                : "2017-05-17 21:55:00"
        , "invoice_address_country"     : "France"
        , "invoice_address_place"       : "75008 Paris"
        , "invoice_address_street1"     : "1 Av. des Champs-Élysées"
        , "invoice_name"                : "M ABC"
        , "invoice_phone1"              : "0123456789"
        , "invoice_phone2"              : None
        , "transport_date"              : "2017-05-18 08:00:00"
        , "transport_type"              : "Delivery"
        , "transport_mode"              : "TNT"
        , "transport_weight"            : "9.000"
        , "transport_unit"              : "kg"
        , "transport_cur"               : "EUR"
        , "delivery_address_country"    : "France"
        , "delivery_address_place"      : "75008 Paris"
        , "delivery_address_street1"    : "1 Av. des Champs-Élysées"
        , "delivery_name"               : "M ABC"
        , "delivery_phone1"             : "0123450689"
        , "customer_ip_address"         : "1.2.3.4"
        , "pmeth_origin"                : "FRA"
        , "pmeth_validity"              : "0121"
        , "pmeth_brand"                 : "MC"
        , "pmeth_bin"                   : "510000"
        , "pmeth_3ds"                   : "-1"
        , "cart_products"               : [ "Product ref #12345" ]
        , "cart_details"                : [{
            "name"                      : "Product ref #12345"
            , "pu"                        : "10.00"
            , "n"                         : "1"
            , "amount"                    : "10.00"
            , "cur"                       : "EUR" 
            }]
        , "cart_n"                      : "15000"
        , "order_payment_accepted"      : "2017-05-17 22:00:00"
        , "amount_pmeth"                : "ABC Payment Service Provider"
        , "amount_discounts"            :  "0.00"
        , "amount_products"             : "20.00"
        , "amount_transport"            : "10.00"
        , "amount_total"                : "30.00"
        , "amount_cur"                  : "EUR"
        }

DUMMY_EVENT_2 = {
          "id"                          : "2"           # a unique id 
        , "email"                       : "def@yahoo.com"
        , "names"                       : "M Def"
        , "account_creation_time"       : "2017-05-17 22:50:00"
        , "account_id"                  : "20"
        , "account_n_fulfilled"         : "1"
        , "account_total_since_created" : "59.40"
        , "account_total_cur"           : "EUR"
        , "invoice_time"                : "2017-05-17 21:55:00"
        , "invoice_address_country"     : "San Francisco, CA 94102"
        , "invoice_address_place"       : "75008 Paris"
        , "invoice_address_street1"     : "944 Market Street, 8th floor"
        , "invoice_name"                : "M Def"
        , "invoice_phone1"              : "+1 111-111-111"
        , "invoice_phone2"              : None
        , "transport_date"              : "2017-05-18 08:00:00"
        , "transport_type"              : "Delivery"
        , "transport_mode"              : "TNT"
        , "transport_weight"            : "9.000"
        , "transport_unit"              : "kg"
        , "transport_cur"               : "EUR"
        , "delivery_address_country"    : "United States"
        , "delivery_address_place"      : "San Francisco, CA 94102"
        , "delivery_address_street1"    : "944 Market Street, 8th floor"
        , "delivery_name"               : "M DEF"
        , "delivery_phone1"             : "+1 111-111-111"
        , "customer_ip_address"         : "4.5.6.7"
        , "pmeth_origin"                : "USA"
        , "pmeth_validity"              : "0221"
        , "pmeth_brand"                 : "MC"
        , "pmeth_bin"                   : "510000"
        , "pmeth_3ds"                   : "-1"
        , "cart_products"               : [ "Product ref #12345" ]
        , "cart_details"                : [{
            "name"                      : "Product ref #12345"
            , "pu"                        : "10.00"
            , "n"                         : "1"
            , "amount"                    : "10.00"
            , "cur"                       : "EUR" 
            }]
        , "cart_n"                      : "15000"
        , "order_payment_accepted"      : "2017-05-17 22:00:00"
        , "amount_pmeth"                : "DEF Payment Service Provider"
        , "amount_discounts"            :  "0.00"
        , "amount_products"             : "20.00"
        , "amount_transport"            : "10.00"
        , "amount_total"                : "30.00"
        , "amount_cur"                  : "EUR"
        }

NOW = datetime.datetime.now()


class UbivarTestCase(unittest2.TestCase):
    RESTORE_ATTRIBUTES = ('api_version', 'api_key', 'client_id')

    def setUp(self):
        super(UbivarTestCase, self).setUp()

        self._ubivar_original_attributes = {}

        for attr in self.RESTORE_ATTRIBUTES:
            self._ubivar_original_attributes[attr] = getattr(ubivar, attr)

        api_base = os.environ.get('UBIVAR_API_BASE')
        if api_base:
            ubivar.api_base = api_base
        ubivar.api_key = os.environ.get('UBIVAR_TEST_TOKEN')

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


class MyCreatable(ubivar.resource.CreatableAPIResource):
    pass


class MyUpdatable(ubivar.resource.UpdatableAPIResource):
    pass


class MyDeletable(ubivar.resource.DeletableAPIResource):
    pass


class MyComposite(ubivar.resource.ListableAPIResource,
                  ubivar.resource.CreatableAPIResource,
                  ubivar.resource.UpdatableAPIResource,
                  ubivar.resource.DeletableAPIResource):
    pass

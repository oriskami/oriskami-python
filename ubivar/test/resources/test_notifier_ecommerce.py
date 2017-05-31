import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase)

DUMMY_ECOMMERCE = {
        "name": "platform 2",
        "is_active": "false"
        }


class UbivarAPIResourcesTests(UbivarTestCase):

    def test_notifier_ecommerce_list(self):
        response = ubivar.NotifierECommerce.list()

        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "notifier_ecommerce")

    def test_notifier_ecommerce_update(self):
        response = ubivar.NotifierECommerce.list()
        originalECommerce = response.data[0]
        
        response = ubivar.NotifierECommerce.update("0", **DUMMY_ECOMMERCE)
        notifierECommerce = response.data[0]
        self.assertEqual(notifierECommerce["name"] , originalECommerce["name"])
        self.assertEqual(notifierECommerce["is_active"], DUMMY_ECOMMERCE["is_active"])

        response = ubivar.NotifierECommerce.update("0", is_active="true")
        notifierECommerce = response.data[0]
        self.assertEqual(notifierECommerce["is_active"]   , "true")
        self.assertEqual(response.object, "notifier_ecommerce")

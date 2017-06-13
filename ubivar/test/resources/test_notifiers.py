import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase, NOW)

class UbivarAPIResourcesTests(UbivarTestCase):

    def test_notifiers_list(self):
        response = ubivar.Notifiers.list()
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "notifiers")

    def test_notifiers_update(self):
        response = ubivar.Notifiers.update("0", is_active="false")
        self.assertEqual(response.data[0]["is_active"], "false")
        self.assertEqual(response.object, "notifiers")

        response = ubivar.Notifiers.update("0", is_active="true")
        self.assertEqual(response.data[0]["is_active"], "true")
        self.assertEqual(response.object, "notifiers")

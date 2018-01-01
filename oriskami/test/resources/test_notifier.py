import os
import oriskami
import warnings
from oriskami.test.helper import (OriskamiTestCase, NOW)

class OriskamiAPIResourcesTests(OriskamiTestCase):

    def test_notifiers_list(self):
        response = oriskami.Notifiers.list()
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "notifiers")

    def test_notifiers_update(self):
        response = oriskami.Notifiers.update("0", is_active="false")
        self.assertEqual(response.data[0]["is_active"], "false")
        self.assertEqual(response.object, "notifiers")

        response = oriskami.Notifiers.update("0", is_active="true")
        self.assertEqual(response.data[0]["is_active"], "true")
        self.assertEqual(response.object, "notifiers")

import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase, NOW)

class UbivarAPIResourcesTests(UbivarTestCase):

    def test_filters_list(self):
        response = ubivar.Filters.list()
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "filters")

    def test_filters_update(self):
        response = ubivar.Filters.update("0", is_active="false")
        self.assertEqual(response.data[0]["is_active"], "false")
        self.assertEqual(response.object, "filters")

        response = ubivar.Filters.update("0", is_active="true")
        self.assertEqual(response.data[0]["is_active"], "true")
        self.assertEqual(response.object, "filters")

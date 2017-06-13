import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase)

class UbivarAPIResourcesTests(UbivarTestCase):

    def test_router_parameter_retrieve(self):
        response = ubivar.RouterParameter.retrieve("0")
        self.assertTrue(hasattr(response.data, "__iter__"))

        routerParameters = response.data
        self.assertTrue(hasattr(routerParameters, "c_per_hour"))
        self.assertTrue(hasattr(routerParameters, "f_cogs"))
        self.assertTrue(hasattr(routerParameters, "reviews_per_hour"))
        self.assertTrue(hasattr(routerParameters, "th0"))

    def test_router_parameter_update(self):
        response = ubivar.RouterParameter.update("0", reviews_per_hour="2")
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertEqual(response.data[0]["reviews_per_hour"], "2")
        response = ubivar.RouterParameter.update("0", reviews_per_hour="4")
        self.assertEqual(response.data[0]["reviews_per_hour"], "4")

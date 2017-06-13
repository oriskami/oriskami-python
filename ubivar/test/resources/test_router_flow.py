import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase, NOW)

class UbivarAPIResourcesTests(UbivarTestCase):

    def test_router_flow_create(self):
        response = ubivar.RouterFlow.create(**{"flow_template": "fraud-risk"})
        routerFlow = response.data[len(response.data)-1]
        self.assertTrue(hasattr(response, "data"))
        self.assertTrue(len(response.data) >= 1)

    def test_router_flow_update(self):
        response = ubivar.RouterFlow.list()

        for i in range(1, len(response.data)):
            response = ubivar.RouterFlow.delete(str(i))

        response = ubivar.RouterFlow.create(**{"flow_template": "fraud-risk"})
        response = ubivar.RouterFlow.create(**{"flow_template": "fraud-risk"})

        ubivar.RouterFlow.update("1", is_active="false")
        response = ubivar.RouterFlow.list()
        self.assertEqual(response.data[1]["is_active"], "false")

        ubivar.RouterFlow.update("1", is_active="true")
        response = ubivar.RouterFlow.list()
        self.assertEqual(response.data[1]["is_active"], "true")

    def test_router_flow_delete(self):
        response = ubivar.RouterFlow.list()

        for i in range(1, len(response.data)):
            response = ubivar.RouterFlow.delete(str(i))
            self.assertEqual(response.object, "router_flows")

    def test_router_flow_list(self):
        response = ubivar.RouterFlow.list()
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "router_flows")
